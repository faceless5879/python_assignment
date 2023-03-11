CREATE TABLE IF NOT EXISTS financial_data
  (
    symbol      varchar(255),
    date      date        ,
    open_price  NUMERIC     ,
    close_price NUMERIC     ,
    volume      integer
  );

ALTER TABLE financial_data ADD CONSTRAINT pkey PRIMARY KEY(symbol, date);