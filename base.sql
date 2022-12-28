CREATE TABLE public.kore_1_Users (
	userId integer NOT NULL PRIMARY KEY,
	age integer NOT NULL
);
	
CREATE TABLE public.kore_1_Items (
	itemId integer NOT NULL PRIMARY KEY,
	price integer NOT NULL
);
	
CREATE TABLE public.kore_1_Purchases (
	purchaseId integer NOT NULL PRIMARY KEY,
	userId integer NOT NULL,
	itemId integer NOT NULL,
	date date NOT NULL,
	CONSTRAINT kore_1_Purchases_fk0 FOREIGN KEY (userId) REFERENCES public.kore_1_Users (userId),
	CONSTRAINT kore_1_Purchases_fk1 FOREIGN KEY (itemId) REFERENCES public.kore_1_Items (itemId)
);

insert into public.kore_1_Users (userId, age) values (generate_series (1000, 1999), trunc(random()*50 + 18));

insert into public.kore_1_Items (itemId, price) values (generate_series (200, 299), trunc(random()*100 + 1));

insert into public.kore_1_Purchases (purchaseId, userId, itemId, date) 
values (generate_series (30000, 39999), trunc(random()*999 + 1000), trunc(random()*99 + 200), ('01/01/2020'::date + trunc(random() * 365) * '1 day'::interval));
insert into public.kore_1_Purchases (purchaseId, userId, itemId, date) 
values (generate_series (40000, 49999), trunc(random()*999 + 1000), trunc(random()*99 + 200), ('01/01/2021'::date + trunc(random() * 365) * '1 day'::interval));