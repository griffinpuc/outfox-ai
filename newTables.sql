-- Table: public.ai_resourcerec_cache

-- DROP TABLE public.ai_resourcerec_cache;

CREATE TABLE IF NOT EXISTS public.ai_resourcerec_cache
(
    id integer NOT NULL DEFAULT nextval('ai_resourcerec_cache_id_seq'::regclass),
    userid integer NOT NULL,
    rec text COLLATE pg_catalog."default" NOT NULL,
    lastchanged time without time zone NOT NULL,
    CONSTRAINT ai_resourcerec_cache_pkey PRIMARY KEY (id),
    CONSTRAINT userconstrainr UNIQUE (userid)
)

TABLESPACE pg_default;

ALTER TABLE public.ai_resourcerec_cache
    OWNER to postgres;
	
	
-- Table: public.ai_userrec_cache

-- DROP TABLE public.ai_userrec_cache;

CREATE TABLE IF NOT EXISTS public.ai_userrec_cache
(
    id integer NOT NULL DEFAULT nextval('ai_userrec_cache_id_seq'::regclass),
    userid integer NOT NULL,
    rec text COLLATE pg_catalog."default" NOT NULL,
    lastchanged time without time zone NOT NULL,
    CONSTRAINT ai_userrec_cache_pkey PRIMARY KEY (id),
    CONSTRAINT userconstrainu UNIQUE (userid)
)

TABLESPACE pg_default;

ALTER TABLE public.ai_userrec_cache
    OWNER to postgres;
	
-- Table: public.ai_grouprec_cache

-- DROP TABLE public.ai_grouprec_cache;

CREATE TABLE IF NOT EXISTS public.ai_grouprec_cache
(
    id integer NOT NULL DEFAULT nextval('ai_grouprec_cache_id_seq'::regclass),
    userid integer NOT NULL,
    rec text COLLATE pg_catalog."default" NOT NULL,
    lastchanged time without time zone NOT NULL,
    CONSTRAINT ai_grouprec_cache_pkey PRIMARY KEY (id),
    CONSTRAINT userconstraint UNIQUE (userid)
)

TABLESPACE pg_default;

ALTER TABLE public.ai_grouprec_cache
    OWNER to postgres;