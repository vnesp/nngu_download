CREATE TABLE IF NOT EXISTS ExamTypes (
    ID              INTEGER     PRIMARY KEY
                                UNIQUE
                                NOT NULL,
    Name            TEXT (100)
);

CREATE TABLE IF NOT EXISTS Faculties (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    Name            TEXT (100)  UNIQUE
                                NOT NULL
);

CREATE TABLE IF NOT EXISTS FormEducations (
    ID              INTEGER     PRIMARY KEY
                                UNIQUE
                                NOT NULL,
    Name            TEXT (100)  NOT NULL
);

CREATE TABLE IF NOT EXISTS FundingSources (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    Name            TEXT (150)  UNIQUE
                                NOT NULL
);

CREATE TABLE IF NOT EXISTS Statuses (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    Name            TEXT (150)  UNIQUE
                                NOT NULL
);

CREATE TABLE IF NOT EXISTS Specializations (
    ID              INTEGER     NOT NULL
                                UNIQUE
                                PRIMARY KEY,
    Cod             TEXT (20)   NOT NULL,
    Name            TEXT (100)  UNIQUE
                                NOT NULL
);

CREATE TABLE IF NOT EXISTS SpecializationVariants (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    SpecID          INTEGER     REFERENCES Specializations(ID)
                                NOT NULL,
    Name            TEXT (100)  NOT NULL
);

CREATE TABLE IF NOT EXISTS Directions (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    FacultyID       INTEGER     REFERENCES Faculties (ID)
                                NOT NULL,
    SpecVarID       INTEGER     REFERENCES SpecializationVariants (ID)
                                NOT NULL,
    FinID           INTEGER     REFERENCES FundingSources (ID)
                                NOT NULL,
    FormID          INTEGER     REFERENCES FormEducations (ID)
                                NOT NULL,
    NumPlaces       INTEGER
);

CREATE TABLE IF NOT EXISTS Abiturients (
    ID              INTEGER     PRIMARY KEY
                                NOT NULL
                                UNIQUE,
    Cod             TEXT (20)   UNIQUE
                                NOT NULL
);

CREATE TABLE IF NOT EXISTS Prioritets (
    ID              INTEGER     UNIQUE
                                NOT NULL
                                PRIMARY KEY,
    AbiturientID    INTEGER     REFERENCES Abiturients (ID)
                                NOT NULL,
    FacultyID       INTEGER     REFERENCES Faculties (ID)
                                NOT NULL,
    SpecID          INTEGER     REFERENCES Specializations (ID)
                                NOT NULL,
    SpecVariantID   INTEGER     REFERENCES SpecializationVariants (ID),
    Prioritet       INTEGER     NOT NULL,
    Status          TEXT (100)  NOT NULL,
    NumSpis         INTEGER     NOT NULL,
    NumIfOrig       INTEGER     NOT NULL,
    FormEdID        INTEGER     REFERENCES FormEducations (ID)
                                NOT NULL,
    FunSourceID     INTEGER     NOT NULL
                                REFERENCES FundingSources (ID)
);

CREATE TABLE IF NOT EXISTS DynamicLists (
    ID              INTEGER     PRIMARY KEY
                                UNIQUE
                                NOT NULL,
    DirectionID     INTEGER     NOT NULL
                                REFERENCES Directions (ID),
    NumGeneral      INTEGER     NOT NULL,
    AbiturientID    INTEGER     NOT NULL
                                REFERENCES Abiturients (ID),
    Consent         TINYINT(1)  NOT NULL,
    NumPrioritet    INTEGER     NOT NULL,
    Mark1           TEXT (20)   NOT NULL,
    Mark2           TEXT (20)   NOT NULL,
    Mark3           TEXT (20)   NOT NULL,
    MarkAchievemnt  TEXT (20)   NOT NULL,
    StatusID        TEXT (100)  REFERENCES Statuses (ID)
);
