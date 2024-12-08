--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.3 (Debian 16.3-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: group; Type: TABLE; Schema: public; Owner: zlata
--

CREATE TABLE public."group" (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


ALTER TABLE public."group" OWNER TO zlata;

--
-- Name: nomenclature; Type: TABLE; Schema: public; Owner: zlata
--

CREATE TABLE public.nomenclature (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb NOT NULL,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone
);


ALTER TABLE public.nomenclature OWNER TO zlata;

--
-- Name: range; Type: TABLE; Schema: public; Owner: zlata
--

CREATE TABLE public.range (
    id text NOT NULL,
    parent_id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


ALTER TABLE public.range OWNER TO zlata;

--
-- Name: recipe; Type: TABLE; Schema: public; Owner: zlata
--

CREATE TABLE public.recipe (
    id text NOT NULL,
    name text NOT NULL,
    document jsonb,
    is_delete boolean DEFAULT false NOT NULL,
    version timestamp without time zone NOT NULL
);


ALTER TABLE public.recipe OWNER TO zlata;

--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: zlata
--

COPY public."group" (id, name, document, is_delete, version) FROM stdin;
\.


--
-- Data for Name: nomenclature; Type: TABLE DATA; Schema: public; Owner: zlata
--

COPY public.nomenclature (id, name, document, is_delete, version) FROM stdin;
\.


--
-- Data for Name: range; Type: TABLE DATA; Schema: public; Owner: zlata
--

COPY public.range (id, parent_id, name, document, is_delete, version) FROM stdin;
\.


--
-- Data for Name: recipe; Type: TABLE DATA; Schema: public; Owner: zlata
--

COPY public.recipe (id, name, document, is_delete, version) FROM stdin;
\.


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: zlata
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: nomenclature nomenclature_pkey; Type: CONSTRAINT; Schema: public; Owner: zlata
--

ALTER TABLE ONLY public.nomenclature
    ADD CONSTRAINT nomenclature_pkey PRIMARY KEY (id);


--
-- Name: range range_pkey; Type: CONSTRAINT; Schema: public; Owner: zlata
--

ALTER TABLE ONLY public.range
    ADD CONSTRAINT range_pkey PRIMARY KEY (id);


--
-- Name: recipe recipe_pkey; Type: CONSTRAINT; Schema: public; Owner: zlata
--

ALTER TABLE ONLY public.recipe
    ADD CONSTRAINT recipe_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

