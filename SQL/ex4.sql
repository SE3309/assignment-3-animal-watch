-- EX4.SQL — Sample Data Inserts for All Tables
-- Assumes EX2.SQL has already created the schema.

USE WildlifeTravelDB;

-- ============================================================
-- 1. USER
-- ============================================================
INSERT INTO User VALUES
('emma@example.com',  '4161231111', 'Emma',  'Wilson',   'hash1', '1995-04-12', 'Canada', '2024-01-10'),
('liam@example.com',  '4161232222', 'Liam',  'Chen',     'hash2', '1998-11-03', 'Canada', '2024-02-15'),
('sophia@example.com','4161233333', 'Sophia','Martinez', 'hash3', '1997-08-20', 'USA',    '2024-02-20'),
('noah@example.com',  '4161234444', 'Noah',  'Patel',    'hash4', '1999-01-05', 'Canada', '2024-03-01'),
('ava@example.com',   '4161235555', 'Ava',   'Singh',    'hash5', '2000-06-15', 'UK',     '2024-03-10');

-- ============================================================
-- 2. CORPORATE ACCOUNT
-- ============================================================
INSERT INTO CorporateAccount VALUES
(101, 'Wildlife Adventures Inc'),
(102, 'EcoTravel Agency'),
(103, 'NatureLens Photography'),
(104, 'SafariWorld Tours'),
(105, 'GlobeTrek Corporate');

-- ============================================================
-- 3. TRIP
-- ============================================================
INSERT INTO Trip VALUES
(201, 'emma@example.com',   101, 'Serengeti Safari',       'Tanzania', '2024-06-01', '2024-06-10', 4500.00),
(202, 'liam@example.com',   102, 'Amazon Expedition',      'Brazil',   '2024-07-15', '2024-07-25', 3800.00),
(203, 'sophia@example.com', NULL,'Rocky Mountain Hike',    'Canada',   '2024-05-20', '2024-05-25', 1200.00),
(204, 'noah@example.com',   103, 'Galápagos Wildlife Tour','Ecuador',  '2024-08-01', '2024-08-08', 5200.00),
(205, 'ava@example.com',    NULL,'Kenya Migration Tour',   'Kenya',    '2024-09-10', '2024-09-18', 4800.00);

-- ============================================================
-- 4. ITINERARY
-- ============================================================
INSERT INTO Itinerary VALUES
(301, 201),
(302, 202),
(303, 203),
(304, 204),
(305, 205);

-- ============================================================
-- 5. ITINERARY DESTINATIONS
-- ============================================================
INSERT INTO ItineraryDestination VALUES
(301, 'Serengeti National Park'),
(301, 'Ngorongoro Crater'),
(302, 'Amazon River Basin'),
(303, 'Lake Louise'),
(304, 'Santa Cruz Island');

-- ============================================================
-- 6. ITINERARY DAILY SCHEDULE
-- ============================================================
INSERT INTO ItineraryDailySchedule VALUES
(301, 1, 'Sunrise game drive'),
(301, 2, 'Big cat tracking'),
(302, 1, 'River canoeing'),
(303, 1, 'Mountain hiking'),
(304, 1, 'Tortoise research walk');

-- ============================================================
-- 7. LOCATION
-- ============================================================
INSERT INTO Location VALUES
(401, 'Serengeti National Park',       'Tanzania', 75.00,  -2.333300,  34.833300,  'National Park', 'Famous for the annual wildebeest migration.'),
(402, 'Amazon Rainforest Reserve',     'Brazil',   40.00,  -3.465300, -62.215900,  'Reserve',       'Diverse rainforest ecosystem.'),
(403, 'Lake Louise',                   'Canada',    0.00,  51.425400, -116.177300, 'Park',          'Stunning glacier-fed lake.'),
(404, 'Galápagos Tortoise Sanctuary',  'Ecuador',  60.00,  -0.743100, -90.321000,  'Sanctuary',     'Home to giant tortoises.'),
(405, 'Maasai Mara Reserve',           'Kenya',    85.00,  -1.406100,  35.020000,  'Reserve',       'Migratory routes of wildebeest.');

-- ============================================================
-- 8. SPECIES
-- ============================================================
INSERT INTO Species VALUES
(501, 'Panthera leo',          'Lion',             'Vulnerable',    'Large African cat species.'),
(502, 'Ara macao',             'Scarlet Macaw',    'Least Concern', 'Colorful parrot found in the Amazon.'),
(503, 'Gopherus agassizii',    'Desert Tortoise',  'Vulnerable',    'Land-dwelling tortoise species.'),
(504, 'Giraffa camelopardalis','Giraffe',          'Vulnerable',    'Tallest land animal.'),
(505, 'Cervus canadensis',     'Elk',              'Least Concern', 'Large deer species in North America.');

-- ============================================================
-- 9. SPECIES HABITAT
-- ============================================================
INSERT INTO SpeciesHabitat VALUES
(501, 'Savannah'),
(502, 'Rainforest'),
(503, 'Dry shrubland'),
(504, 'Grassland'),
(505, 'Mountain forest');

-- ============================================================
-- 10. SIGHTING
-- ============================================================
INSERT INTO Sighting VALUES
(601, 501, 401, 301, '2024-06-02 07:30:00', 'emma@example.com'),
(602, 502, 402, 302, '2024-07-16 14:00:00', 'liam@example.com'),
(603, 505, 403, 303, '2024-05-21 10:15:00', 'sophia@example.com'),
(604, 503, 404, 304, '2024-08-02 12:45:00', 'noah@example.com'),
(605, 504, 405, 305, '2024-09-11 16:20:00', 'ava@example.com');

-- ============================================================
-- 11. REVIEW
-- ============================================================
INSERT INTO Review VALUES
(701, 'emma@example.com',   401, 5, 'Amazing wildlife experience!',  '2024-06-12', 22),
(702, 'liam@example.com',   402, 4, 'Beautiful birds everywhere.',   '2024-07-30', 10),
(703, 'sophia@example.com', 403, 5, 'Breathtaking views.',           '2024-05-27', 18),
(704, 'noah@example.com',   404, 4, 'Saw giant tortoises!',          '2024-08-10', 15),
(705, 'ava@example.com',    405, 5, 'Incredible migration event.',   '2024-09-22', 30);

-- ============================================================
-- 12. REVIEW PHOTOS
-- ============================================================
INSERT INTO ReviewPhoto VALUES
(701, 1, 'lion_photo1.jpg'),
(702, 1, 'macaw_colours.jpg'),
(703, 1, 'lake_louise_view.jpg'),
(704, 1, 'tortoise_closeup.jpg'),
(705, 1, 'migration_wildebeest.jpg');
