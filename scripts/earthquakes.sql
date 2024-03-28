CREATE TABLE public.earthquakes (
    generated TIMESTAMP WITH TIME ZONE,
    metadata_url TEXT,
    metadata_title TEXT,
    metadata_status INT,
    api TEXT,
    count INT,
    mag FLOAT,
    place TEXT,
    time TIMESTAMP WITH TIME ZONE,
    updated TIMESTAMP WITH TIME ZONE,
    tz TEXT,
    url TEXT,
    detail TEXT,
    felt INT,
    cdi FLOAT,
    mmi FLOAT,
    alert TEXT,
    status TEXT,
    tsunami INT,
    sig INT,
    net TEXT,
    code TEXT,
    ids TEXT,
    sources TEXT,
    types TEXT,
    nst INT,
    dmin FLOAT,
    rms FLOAT,
    gap INT,
    magType TEXT,
    type TEXT,
    title TEXT,
    geometry_coordinates FLOAT[],
    longitude FLOAT,
    latitude FLOAT,
    radius FLOAT,
    id TEXT
);
