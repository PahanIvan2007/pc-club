INSERT INTO games (name, short_name, icon) VALUES
('Counter-Strike 2', 'CS2', 'cs.png'),
('Dota 2', 'Dota', 'dota.png'),
('Valorant', 'VAL', 'val.png'),
('PUBG', 'PUBG', 'pubg.png');

INSERT INTO players (name, nickname, total_hours) VALUES
('Ivan Petrov', 'ShadowKiller', 352),
('Alexey Smirnov', 'ProGamer99', 287),
('Dmitry Ivanov', 'NightHawk', 245),
('Sergey Kuznetsov', 'CyberWolf', 312),
('Andrey Popov', 'FlameStrike', 198),
('Maxim Vasilyev', 'IceBreaker', 276),
('Egor Sokolov', 'DarkLord', 334),
('Nikita Morozov', 'SilverArrow', 189),
('Artem Novikov', 'ThunderBolt', 267),
('Vladimir Fedorov', 'Stealth', 156);

INSERT INTO activity_log (player_id, game_id, hours) VALUES
(1, 1, 120), (1, 2, 80), (1, 3, 152),
(2, 1, 200), (2, 2, 87),
(3, 2, 180), (3, 4, 65),
(4, 1, 150), (4, 3, 162),
(5, 2, 140), (5, 4, 58),
(6, 1, 176), (6, 3, 100),
(7, 2, 210), (7, 1, 124),
(8, 3, 130), (8, 4, 59),
(9, 1, 190), (9, 2, 77),
(10, 3, 100), (10, 4, 56);

INSERT INTO tournaments (title, game_id, date, prize_pool, status) VALUES
('CS2 Summer Cup', 1, '2026-07-15 17:00', 50000, 'upcoming'),
('Dota 2 Champions', 2, '2026-07-20 16:00', 75000, 'upcoming'),
('Valorant Open', 3, '2026-06-28 15:00', 30000, 'upcoming'),
('PUBG Battle Royale', 4, '2026-08-01 18:00', 40000, 'upcoming');

INSERT INTO tournament_participants (tournament_id, player_id) VALUES
(1, 1), (1, 2), (1, 4), (1, 6), (1, 7), (1, 9),
(2, 3), (2, 5), (2, 7), (2, 9),
(3, 1), (3, 4), (3, 6), (3, 8), (3, 10),
(4, 3), (4, 5), (4, 8), (4, 10);
