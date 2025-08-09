from datetime import datetime
from http.server import BaseHTTPRequestHandler
import json
import os
import requests

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            # 强制禁用缓存
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.end_headers()

            github_token = os.environ.get('GITHUB_TOKEN')
            repo_name = os.environ.get('GITHUB_REPOSITORY', 'derekguo0/design-news-aggregator')

            status_payload = {
                'deployment_type': 'serverless',
                'timestamp': datetime.now().isoformat(),
                'has_github_token': bool(github_token),
                'repo': repo_name
            }

            if github_token:
                try:
                    # 查询最近一次 deploy 工作流运行状态
                    url = f"https://api.github.com/repos/{repo_name}/actions/workflows/deploy.yml/runs?per_page=1"
                    headers = {
                        'Authorization': f'token {github_token}',
                        'Accept': 'application/vnd.github.v3+json',
                        'X-GitHub-Api-Version': '2022-11-28'
                    }
                    resp = requests.get(url, headers=headers, timeout=10)
                    if resp.status_code == 200:
                        data = resp.json()
                        runs = data.get('workflow_runs', [])
                        if runs:
                            run = runs[0]
                            status_payload.update({
                                'status': run.get('status'),  # queued, in_progress, completed
                                'conclusion': run.get('conclusion'),  # success, failure, cancelled
                                'run_id': run.get('id'),
                                'html_url': run.get('html_url'),
                                'created_at': run.get('created_at'),
                                'updated_at': run.get('updated_at'),
                                'message': 'Fetched latest workflow run'
                            })
                        else:
                            status_payload.update({
                                'status': 'unknown',
                                'message': 'No workflow runs found'
                            })
                    else:
                        status_payload.update({
                            'status': 'error',
                            'message': f'GitHub API error: HTTP {resp.status_code}'
                        })
                except requests.exceptions.Timeout:
                    status_payload.update({'status': 'error', 'message': 'GitHub API timeout'})
                except requests.exceptions.ConnectionError:
                    status_payload.update({'status': 'error', 'message': 'Network connection error to GitHub API'})
                except Exception as e:
                    status_payload.update({'status': 'error', 'message': f'Unexpected error: {str(e)}'})
            else:
                status_payload.update({
                    'status': 'manual',
                    'message': 'GITHUB_TOKEN not configured; cannot query workflow status'
                })

            self.wfile.write(json.dumps(status_payload, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': str(e)}, ensure_ascii=False).encode('utf-8'))
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 