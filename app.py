import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

DB_PARAMS = {
    'dbname': 'pc_club',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

def get_db():
    return psycopg2.connect(**DB_PARAMS, cursor_factory=psycopg2.extras.RealDictCursor)

@app.route('/api/stats')
def stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as total FROM players")
    players = cur.fetchone()['total']
    cur.execute("SELECT COUNT(*) as total FROM tournaments")
    tournaments = cur.fetchone()['total']
    cur.close()
    conn.close()
    return jsonify({'total_players': players, 'total_tournaments': tournaments})

@app.route('/api/top-players')
def top_players():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, nickname, total_hours FROM players ORDER BY total_hours DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/players')
def players():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.nickname, p.total_hours,
               COALESCE(json_agg(json_build_object('game', g.short_name, 'hours', al.hours))
                        FILTER (WHERE g.id IS NOT NULL), '[]') as games
        FROM players p
        LEFT JOIN activity_log al ON p.id = al.player_id
        LEFT JOIN games g ON al.game_id = g.id
        GROUP BY p.id ORDER BY p.total_hours DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/tournaments')
def tournaments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, t.title, g.name as game_name, g.short_name,
               t.date, t.prize_pool, t.status
        FROM tournaments t JOIN games g ON t.game_id = g.id
        ORDER BY t.date
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route('/api/tournaments/<int:tid>')
def tournament_detail(tid):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, t.title, g.name as game_name, g.short_name,
               t.date, t.prize_pool, t.status
        FROM tournaments t JOIN games g ON t.game_id = g.id
        WHERE t.id = %s
    """, (tid,))
    tournament = cur.fetchone()
    if not tournament:
        return jsonify({'error': 'Турнир не найден'}), 404

    cur.execute("""
        SELECT p.id, p.name, p.nickname, tp.place, tp.prize
        FROM tournament_participants tp
        JOIN players p ON tp.player_id = p.id
        WHERE tp.tournament_id = %s
        ORDER BY tp.place NULLS LAST
    """, (tid,))
    participants = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({'tournament': tournament, 'participants': participants})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    try:
        return send_from_directory('static', path)
    except:
        return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
