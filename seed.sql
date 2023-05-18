--
-- PostgreSQL database dump
--

-- Dumped from database version 13.11
-- Dumped by pg_dump version 14.8 (Homebrew)

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
-- Name: listings; Type: TABLE; Schema: public; Owner: mpappas
--

CREATE TABLE public.listings (
    id integer NOT NULL,
    url character varying NOT NULL,
    title character varying NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


-- ALTER TABLE public.listings OWNER TO mpappas;

--
-- Name: listings_id_seq; Type: SEQUENCE; Schema: public; Owner: mpappas
--

CREATE SEQUENCE public.listings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.listings_id_seq OWNER TO mpappas;

--
-- Name: listings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mpappas
--

ALTER SEQUENCE public.listings_id_seq OWNED BY public.listings.id;


--
-- Name: urls; Type: TABLE; Schema: public; Owner: mpappas
--

CREATE TABLE public.urls (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    search_url text NOT NULL,
    active boolean
);


-- ALTER TABLE public.urls OWNER TO mpappas;

--
-- Name: urls_id_seq; Type: SEQUENCE; Schema: public; Owner: mpappas
--

CREATE SEQUENCE public.urls_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


-- ALTER TABLE public.urls_id_seq OWNER TO mpappas;

--
-- Name: urls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mpappas
--

ALTER SEQUENCE public.urls_id_seq OWNED BY public.urls.id;


--
-- Name: listings id; Type: DEFAULT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.listings ALTER COLUMN id SET DEFAULT nextval('public.listings_id_seq'::regclass);


--
-- Name: urls id; Type: DEFAULT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.urls ALTER COLUMN id SET DEFAULT nextval('public.urls_id_seq'::regclass);


--
-- Data for Name: listings; Type: TABLE DATA; Schema: public; Owner: mpappas
--

COPY public.listings (id, url, title, "timestamp") FROM stdin;
\.


--
-- Data for Name: urls; Type: TABLE DATA; Schema: public; Owner: mpappas
--

COPY public.urls (id, name, search_url, active) FROM stdin;
\.


--
-- Name: listings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mpappas
--

SELECT pg_catalog.setval('public.listings_id_seq', 1, false);


--
-- Name: urls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mpappas
--

SELECT pg_catalog.setval('public.urls_id_seq', 1, false);


--
-- Name: listings listings_pkey; Type: CONSTRAINT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.listings
    ADD CONSTRAINT listings_pkey PRIMARY KEY (id);


--
-- Name: listings listings_url_key; Type: CONSTRAINT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.listings
    ADD CONSTRAINT listings_url_key UNIQUE (url);


--
-- Name: urls urls_name_key; Type: CONSTRAINT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_name_key UNIQUE (name);


--
-- Name: urls urls_pkey; Type: CONSTRAINT; Schema: public; Owner: mpappas
--

ALTER TABLE ONLY public.urls
    ADD CONSTRAINT urls_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

