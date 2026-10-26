"""Aggregate-only local audit. Never prints or writes a credential value."""
import json
import re
import subprocess
from pathlib import Path
from dotenv import dotenv_values

root = Path(__file__).resolve().parents[2]
key = (dotenv_values(root / '.env').get('OPENAI_API_KEY') or '').encode()
assert key, 'Private configuration is absent; value not displayed.'
pattern = re.compile(rb'sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
files = git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0')
paths = [root / f.decode() for f in files if f and (root / f.decode()).is_file()]
working_key_hits = sum(key in p.read_bytes() for p in paths)
working_pattern_hits = sum(bool(pattern.search(p.read_bytes())) for p in paths)
objects = git('rev-list', '--objects', '--all').splitlines()
proc = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
blobs = history_key_hits = history_pattern_hits = 0
for line in objects:
    proc.stdin.write(line.split(b' ', 1)[0] + b'\n')
    proc.stdin.flush()
    header = proc.stdout.readline().split()
    assert len(header) == 3
    data = proc.stdout.read(int(header[2]))
    assert proc.stdout.read(1) == b'\n'
    if header[1] == b'blob':
        blobs += 1
        history_key_hits += key in data
        history_pattern_hits += bool(pattern.search(data))
proc.stdin.close()
assert proc.wait() == 0
env_tracked = b'.env' in git('ls-files', '-z').split(b'\0')
env_ignored = subprocess.run(['git', 'check-ignore', '-q', '.env'], cwd=root).returncode == 0
freeze = git('rev-parse', 'eval-freeze').decode().strip()
historical_paths = ['heldout', 'eval/heldout-run-started.json', 'HELDOUT_RESULTS.md', 'results/northeast-stress', 'results/m4-verification', 'results/m4-ablations']
history_unchanged = not git('diff', '7c93a86', '--', *historical_paths).strip()
result = {
    'audited_head': git('rev-parse', 'HEAD').decode().strip(),
    'working_files_scanned': len(paths), 'history_blobs_scanned': blobs,
    'configured_key_working_matches': working_key_hits, 'credential_like_working_files': working_pattern_hits,
    'configured_key_history_matches': history_key_hits, 'credential_like_history_blobs': history_pattern_hits,
    'env_tracked': env_tracked, 'env_ignored': env_ignored, 'env_mode': oct((root / '.env').stat().st_mode & 0o777),
    'freeze_tag': freeze, 'freeze_tag_unchanged': freeze == '24d729a540ed3913ced09ee42af89765fd921c4b',
    'historical_evaluations_unchanged': history_unchanged,
    'secret_values_printed_or_saved': False,
    'scope': 'Current configured key equality and long OpenAI-like token patterns in reachable Git blobs and tracked/unignored working files. Does not prove absence of every possible credential or audit host/provider retention.'
}
out = Path(__file__).with_name('security.json')
out.write_text(json.dumps(result, indent=2) + '\n')
assert not any((working_key_hits, working_pattern_hits, history_key_hits, history_pattern_hits, env_tracked))
assert env_ignored and result['env_mode'] == '0o600' and result['freeze_tag_unchanged'] and history_unchanged
print(json.dumps(result, indent=2))
