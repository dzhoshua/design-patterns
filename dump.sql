
CREATE TABLE public."group" (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


CREATE TABLE public.nomenclature (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb NOT NULL,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone
);


CREATE TABLE public.range (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


CREATE TABLE public.recipe (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


CREATE TABLE public.warehouse (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb NOT NULL,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone
);


CREATE TABLE public.warehouse_transaction (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb NOT NULL,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone
);


ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.nomenclature
    ADD CONSTRAINT nomenclature_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.range
    ADD CONSTRAINT range_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.warehouse
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);


ALTER TABLE ONLY public.warehouse_transaction
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);