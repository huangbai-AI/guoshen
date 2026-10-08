import copy, json, tempfile, unittest, shutil
import runpy, sys
from pathlib import Path
from unittest.mock import patch
from resource_paths import resource_path
from build_review_context import ROOT, build, assess
from validate_framework import validate
from scan_candidates import detect, scan
class FrameworkTests(unittest.TestCase):
    def test_utf8_file_io_with_gbk_default(self):
        # Emulate a non-UTF-8 file default even on UTF-8 CI hosts.
        def gbk_text_encoding(encoding, stacklevel=2):
            return 'gbk' if encoding is None else encoding

        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            profile = json.loads(resource_path(ROOT,'profiles/strict-address.json').read_text(encoding='utf-8'))
            profile['profile_type'] = '自定义配置😊'
            profile_path = temp / 'profile.json'
            profile_path.write_text(json.dumps(profile, ensure_ascii=False), encoding='utf-8')
            row = {'start':0, 'end':1, 'channel':'screen_text', 'text':'资料😊请加微信'}
            evidence = temp / 'evidence.json'
            evidence.write_text(json.dumps([row], ensure_ascii=False), encoding='utf-8')
            expected_counts = validate()
            for script in ['build_review_context.py', 'scan_candidates.py', 'validate_framework.py']:
                with self.subTest(script=script):
                    output = temp / (script + '.json')
                    if script.startswith('build'):
                        args = ['--platforms','douyin','--as-of','2026-09-07',
                                '--profile',str(profile_path),'--out',str(output)]
                    elif script.startswith('scan'):
                        args = [str(evidence),'--platforms','douyin',
                                '--profile',str(profile_path),'--out',str(output)]
                    else:
                        args = []
                    with patch('io.text_encoding', gbk_text_encoding):
                        if script.startswith('validate'):
                            self.assertEqual(validate(), expected_counts)
                        else:
                            with patch.object(sys, 'argv', [script, *args]):
                                runpy.run_path(str(ROOT / 'scripts' / script), run_name='__main__')
                    if script.startswith('build'):
                        result = json.loads(output.read_bytes().decode('utf-8'))
                        self.assertEqual(result['profile'], profile)
                        self.assertEqual({r['scope'] for r in result['rules']}, {'common','douyin'})
                    elif script.startswith('scan'):
                        result = json.loads(output.read_bytes().decode('utf-8'))
                        self.assertTrue(result['candidates'])
                        self.assertTrue(all(c['text'] == row['text'] for c in result['candidates']))
    def test_platform_isolation(self):
        for platform in ['xiaohongshu','douyin','bilibili','wechat_channels']:
            c=build([platform],'2026-09-07')
            self.assertEqual({r['scope'] for r in c['rules']},{'common',platform})
    def test_candidate_platform_filter_and_host(self):
        self.assertTrue(any(x['kind']=='suspected_url' for x in detect('demo.example.host')))
        profile=json.loads(resource_path(ROOT,'profiles/strict-address.json').read_text(encoding='utf-8'))
        profile['default_platforms']=['bilibili']
        result=scan([{'start':0,'end':1,'channel':'screen_text','text':'example.com'}],profile)
        self.assertEqual(set(result[0]['platform_candidates']),{'bilibili'})
    def test_unknown(self):
        with self.assertRaises(ValueError): build(['unknown'],'2026-09-07')
    def test_profiles(self):
        self.assertEqual(build(['douyin'],'2026-09-07')['profile']['strict_visual_address_platforms'],[])
        self.assertIn('douyin',build(['douyin'],'2026-09-07',profile=ROOT/'profiles/strict-address.json')['profile']['strict_visual_address_platforms'])
    def test_dates(self):
        r=json.loads(resource_path(ROOT,'rules/common/rules.json').read_text(encoding='utf-8'))[0]
        self.assertTrue(assess(r,'2026-11-01')['uncertainties'])
        self.assertTrue(any('历史' in x for x in assess(r,'2026-08-01')['uncertainties']))
        r.update(effective_from='2026-09-01',effective_to='2026-09-30')
        self.assertIsNone(assess(r,'2026-08-31')); self.assertIsNone(assess(r,'2026-10-01'))
        self.assertIsNotNone(assess(r,'2026-09-30'))
        r['status']='retired'; self.assertIsNone(assess(r,'2026-09-07'))
    def test_source_gaps(self):
        c=build(['douyin'],'2026-09-07')
        pending=next(r for r in c['rules'] if r['id']=='GS-D004')
        self.assertTrue(pending['uncertainties']); self.assertEqual(pending['status'],'verification_needed')
        w=build(['wechat_channels'],'2026-09-07')
        self.assertTrue(all(r['sources'][0]['evidence_status']=='官方全文' for r in w['rules'] if r['scope']=='wechat_channels'))
    def test_invalid_data(self):
        for mutation in ['duplicate','fake_source','synthetic_evidence']:
            with tempfile.TemporaryDirectory() as temp:
                dst=Path(temp)/'repo'; shutil.copytree(ROOT,dst,ignore=shutil.ignore_patterns('.git','models','__pycache__'))
                p=resource_path(dst,'rules/common/rules.json'); data=json.loads(p.read_text(encoding='utf-8'))
                if mutation=='duplicate': data.append(copy.deepcopy(data[0]))
                elif mutation=='fake_source': data[0]['source_ids']=['MISSING']
                else: data[0]['case_ids']=['EX-0001']
                p.write_text(json.dumps(data), encoding='utf-8')
                with self.assertRaises(AssertionError): validate(dst)
    def test_examples_are_not_empirical(self):
        self.assertEqual(validate()[2],0)
if __name__=='__main__': unittest.main()
