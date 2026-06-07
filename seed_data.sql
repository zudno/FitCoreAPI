-- ============================================================
-- SEED: Muscle Groups + Exercises básicos
-- Ejecutar después de que SQLModel haya creado las tablas
-- ============================================================

-- ─────────────────────────────────────────────
-- MUSCLE GROUPS
-- ─────────────────────────────────────────────

INSERT INTO muscle_groups (id, name) VALUES
  ('00000001-0000-0000-0000-000000000001', 'Pectorales'),
  ('00000001-0000-0000-0000-000000000002', 'Espalda'),
  ('00000001-0000-0000-0000-000000000003', 'Hombros'),
  ('00000001-0000-0000-0000-000000000004', 'Bíceps'),
  ('00000001-0000-0000-0000-000000000005', 'Tríceps'),
  ('00000001-0000-0000-0000-000000000006', 'Piernas'),
  ('00000001-0000-0000-0000-000000000007', 'Glúteos'),
  ('00000001-0000-0000-0000-000000000008', 'Abdominales'),
  ('00000001-0000-0000-0000-000000000009', 'Pantorrillas'),
  ('00000001-0000-0000-0000-000000000010', 'Antebrazos'),
  ('00000001-0000-0000-0000-000000000011', 'Trapecio'),
  ('00000001-0000-0000-0000-000000000012', 'Cardio')
ON CONFLICT (name) DO NOTHING;


-- ─────────────────────────────────────────────
-- EXERCISES
-- user_id = NULL → ejercicios globales del sistema
-- ─────────────────────────────────────────────

-- ── PECTORALES ──────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press de Banca con Barra',         'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press de Banca con Mancuernas',    'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press Inclinado con Barra',        'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press Inclinado con Mancuernas',   'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press Declinado con Barra',        'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Aperturas con Mancuernas',         'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Aperturas en Polea',               'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Fondos en Paralelas',              'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Flexiones',                        'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000001', NULL, 'Press en Máquina Pecho',           'Máquina',        NOW())
ON CONFLICT DO NOTHING;

-- ── ESPALDA ─────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Peso Muerto',                      'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Dominadas',                        'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Remo con Barra',                   'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Remo con Mancuerna',               'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Remo en Polea Baja',               'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Jalón al Pecho en Polea',          'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Jalón al Pecho Agarre Cerrado',    'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Pull-over con Mancuerna',          'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Remo en Máquina',                  'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000002', NULL, 'Hiperextensiones',                 'Peso Corporal',  NOW())
ON CONFLICT DO NOTHING;

-- ── HOMBROS ─────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Press Militar con Barra',          'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Press de Hombros con Mancuernas',  'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Elevaciones Laterales',            'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Elevaciones Frontales',            'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Pájaros (Elevaciones Posteriores)','Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Press Arnold',                     'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Elevaciones Laterales en Polea',   'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000003', NULL, 'Face Pull',                        'Polea',          NOW())
ON CONFLICT DO NOTHING;

-- ── BÍCEPS ──────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl con Barra',                   'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl con Mancuernas',              'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl Martillo',                    'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl Concentrado',                 'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl en Polea',                    'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl con Barra Z (EZ)',            'Barra EZ',       NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000004', NULL, 'Curl en Banco Scott',              'Máquina',        NOW())
ON CONFLICT DO NOTHING;

-- ── TRÍCEPS ─────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Press Francés con Barra',          'Barra EZ',       NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Extensión de Tríceps en Polea',    'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Fondos en Banco',                  'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Patada de Tríceps',                'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Extensión sobre la Cabeza',        'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Press Cerrado con Barra',          'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000005', NULL, 'Tríceps en Máquina',               'Máquina',        NOW())
ON CONFLICT DO NOTHING;

-- ── PIERNAS ─────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Sentadilla con Barra',             'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Sentadilla Hack',                  'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Prensa de Piernas',                'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Extensión de Cuádriceps',          'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Curl de Isquiotibiales',           'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Zancadas con Mancuernas',          'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Peso Muerto Rumano',               'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Sentadilla Búlgara',               'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Leg Press',                        'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000006', NULL, 'Sentadilla Goblet',                'Mancuernas',     NOW())
ON CONFLICT DO NOTHING;

-- ── GLÚTEOS ─────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000007', NULL, 'Hip Thrust con Barra',             'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000007', NULL, 'Patada de Glúteo en Polea',        'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000007', NULL, 'Abducción de Cadera en Máquina',   'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000007', NULL, 'Sentadilla Sumo',                  'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000007', NULL, 'Puente de Glúteo',                 'Peso Corporal',  NOW())
ON CONFLICT DO NOTHING;

-- ── ABDOMINALES ─────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Crunch Abdominal',                 'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Plancha',                          'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Elevación de Piernas Colgado',     'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Rueda Abdominal',                  'Rueda',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Crunch en Polea',                  'Polea',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Rotación Rusa',                    'Peso Corporal',  NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000008', NULL, 'Bicicleta Abdominal',              'Peso Corporal',  NOW())
ON CONFLICT DO NOTHING;

-- ── PANTORRILLAS ────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000009', NULL, 'Elevación de Talones de Pie',      'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000009', NULL, 'Elevación de Talones Sentado',     'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000009', NULL, 'Elevación de Talones con Barra',   'Barra',          NOW())
ON CONFLICT DO NOTHING;

-- ── ANTEBRAZOS ──────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000010', NULL, 'Curl de Muñeca con Barra',         'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000010', NULL, 'Extensión de Muñeca',              'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000010', NULL, 'Agarre de Barra (Farmer Walk)',    'Barra',          NOW())
ON CONFLICT DO NOTHING;

-- ── TRAPECIO ────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000011', NULL, 'Encogimientos con Barra',          'Barra',          NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000011', NULL, 'Encogimientos con Mancuernas',     'Mancuernas',     NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000011', NULL, 'Remo al Mentón',                   'Barra',          NOW())
ON CONFLICT DO NOTHING;

-- ── CARDIO ──────────────────────────────────

INSERT INTO exercises (id, muscle_group_id, user_id, name, equipment, created_at) VALUES
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Caminadora',                       'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Bicicleta Estática',               'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Elíptica',                         'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Remo (Ergómetro)',                  'Máquina',        NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Saltar la Cuerda',                 'Cuerda',         NOW()),
  (gen_random_uuid(), '00000001-0000-0000-0000-000000000012', NULL, 'Burpees',                          'Peso Corporal',  NOW())
ON CONFLICT DO NOTHING;
