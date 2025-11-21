-- ============================================================
-- EX1.SQL — Three Different INSERT Styles into Review
-- Assumes EX2.SQL (schema) and EX3.SQL (initial data) are done.
-- ============================================================
USE WildlifeTravelDB; 

-- ------------------------------------------------------------
-- TYPE 1: Standard INSERT ... VALUES (single row)
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

-- Expected Workbench status message:
-- 1 row(s) affected

-- ------------------------------------------------------------
-- TYPE 2: MySQL INSERT ... SET syntax (also inserts into Review)
-- ------------------------------------------------------------
INSERT INTO Review
SET
    reviewID    = 707,
    userEmail   = 'liam@example.com',
    locationID  = 401,
    rating      = 4,
    reviewText  = 'great lion sightings near the river.',
    datePosted  = '2024-10-02',
    helpfulCount = 0;

-- Expected Workbench status message:
-- 1 row(s) affected

-- ------------------------------------------------------------
-- TYPE 3: INSERT ... SELECT (creates a review from data in User)
-- ------------------------------------------------------------
-- Create a new review for a Canadian user automatically,
-- building the review text from the User table.

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

-- Expected Workbench status message:
-- 1 row(s) affected

-- ------------------------------------------------------------
-- SEE THE RESULTING RELATION
-- ------------------------------------------------------------
SELECT * FROM Review
ORDER BY reviewID;