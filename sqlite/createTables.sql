CREATE TABLE Company
(
    company_ID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    website TEXT,
    ceo TEXT,
    employees INTEGER,
    sector_ID INTEGER,
    industry_ID INTEGER,
    ceo_title_ID INTEGER,
    UNIQUE(title),
    FOREIGN KEY (sector_ID) REFERENCES Sector(sector_ID),
    FOREIGN KEY (industry_ID) REFERENCES Industry(industry_ID),
    FOREIGN KEY (ceo_title_ID) REFERENCES CeoTitle(ceo_title_ID),
    FOREIGN KEY (company_ID) REFERENCES HQ(company_ID),
    FOREIGN KEY (company_ID) REFERENCES Alias(company_ID),
    FOREIGN KEY (company_ID) REFERENCES YearRank(company_ID)
);

CREATE TABLE HQ
(
    company_ID INTEGER PRIMARY KEY,
    street TEXT,
    city TEXT,
    hq_state TEXT,
    zip TEXT,
    phone TEXT,
    UNIQUE(phone)
);

CREATE TABLE Alias
(
    company_ID INTEGER PRIMARY KEY,
    ticker TEXT,
    full_name TEXT,
    UNIQUE(full_name)
);

CREATE TABLE Sector
(
    sector_ID INTEGER PRIMARY KEY,
    sector TEXT,
    UNIQUE(sector)
);

CREATE TABLE Industry
(
    industry_ID INTEGER PRIMARY KEY,
    industry TEXT,
    UNIQUE(industry)
);

CREATE TABLE CeoTitle
(
    ceo_title_ID INTEGER PRIMARY KEY,
    title TEXT,
    UNIQUE(title)
);

CREATE TABLE YearRank
(
    company_ID INTEGER NOT NULL,
    year INTEGER NOT NULL,
    rank INTEGER,
    revenues DECIMAL(8, 2),
    profits DECIMAL(8, 2),
    assets DECIMAL(8, 2),
    PRIMARY KEY (company_ID, year)
);
