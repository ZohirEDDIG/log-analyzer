import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

PATHS = [
    ('/', 30),
    ('/login', 15),
    ('/api/users', 12),
    ('/api/products', 12),
    ('/search', 8),
    ('/cart', 6),
    ('/checkout', 4),
    ('/admin', 3),
    ('/static/app.js', 5),
    ('/static/style.css', 5),
]

METHODS = [('GET', 80), ('POST', 15), ('PUT', 3), ('DELETE', 2)]

STATUSES = [
    (200, 70),
    (301, 5),
    (304, 6),
    (400, 3),
    (401, 4),
    (403, 3),
    (404, 5),
    (500, 3),
    (502, 1),
]

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1',
    'Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0',
    'curl/8.4.0',
    'python-requests/2.31.0',
]

ATTACKER_IPS = ['45.33.32.156', '185.220.101.5', '103.21.244.9']

def weighted(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights)[0]

def random_ip():
    return '.'.join(str(random.randint(1, 254)) for _ in range(4))

def make_line(ts):
    if random.random() < 0.05:
        ip = random.choice(ATTACKER_IPS)
        method, path = 'POST', '/login'
        status = random.choice([401, 403])
    else:
        ip = random_ip() 
        method = weighted(METHODS)
        path = weighted(PATHS)
        status = weighted(STATUSES)

    size = random.randint(200, 50000)
    agent = random.choice(USER_AGENTS)
    time_str = ts.strftime('%d/%b/%Y:%H:%M:%S %z')

    return f'{ip} - - [{time_str}] "{method} {path} HTTP/1.1 {status} {size} "-" "{agent}"'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--lines', type=int, default=10000)
    parser.add_argument('-o', '--output', default='../sample_logs/access.log')
    parser.add_argument('--days', type=int, default=3, help='spread logs over N days')
    args = parser.parse_args()

    end = datetime.now(timezone.utc)
    start = end - timedelta(days = args.days)
    span = (end - start).total_seconds()

    times =  sorted(start + timedelta(seconds=random.random() * span) for _ in range(args.lines))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w') as f:
        for ts in times:
            f.write(make_line(ts) + '\n')

    print(f"Wrote {args.lines} lines to {out}")


if __name__ == '__main__':
    main() 