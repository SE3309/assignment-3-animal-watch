-- EX3.SQL — Three Different INSERT Styles into Review
-- Assumes EX2.SQL (schema) and EX4.SQL (base data) have already been run.

USE WildlifeTravelDB;

-- ------------------------------------------------------------
-- TYPE 1: Standard INSERT ... VALUES (single-row)
-- ------------------------------------------------------------
INSERT INTO Review (
    reviewID, userEmail, locationID, rating,
    reviewText, datePosted, helpfulCount
)
VALUES (
    706,
    'emma@example.com',
    405,
    5,
    'Returned for the migration – even better the second time!',
    '2024-10-01',
    4
);

-- ------------------------------------------------------------
-- TYPE 2: MySQL INSERT ... SET syntax
-- ------------------------------------------------------------
INSERT INTO Review
SET
    reviewID     = 707,
    userEmail    = 'liam@example.com',
    locationID   = 401,
    rating       = 4,
    reviewText   = 'Great lion sightings near the river.',
    datePosted   = '2024-10-02',
    helpfulCount = 0;

-- ------------------------------------------------------------
-- TYPE 3: INSERT ... SELECT
-- Create a new review for a specific user (Sophia) using data
-- pulled from the User table.
-- ------------------------------------------------------------
INSERT INTO Review (
    reviewID, userEmail, locationID, rating,
    reviewText, datePosted, helpfulCount
)
SELECT
    708 AS reviewID,
    u.userEmail,
    403 AS locationID,          -- Lake Louise
    5   AS rating,
    CONCAT('Auto-generated review for ', u.firstName,
           ': Lake Louise was stunning!') AS reviewText,
    '2024-10-03' AS datePosted,
    1   AS helpfulCount
FROM User u
WHERE u.userEmail = 'sophia@example.com';

-- ------------------------------------------------------------
-- SEE THE RESULTING RELATION (optional for checking)
-- ------------------------------------------------------------
SELECT * FROM Review
ORDER BY reviewID;

