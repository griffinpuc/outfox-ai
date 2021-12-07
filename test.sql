--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- Started on 2021-12-07 16:52:14

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

--
-- TOC entry 679 (class 1247 OID 43906)
-- Name: enum_friends_status; Type: TYPE; Schema: public; Owner: salcosser
--

CREATE TYPE public.enum_friends_status AS ENUM (
    'a',
    'r',
    'p'
);


ALTER TYPE public.enum_friends_status OWNER TO salcosser;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 207 (class 1259 OID 43881)
-- Name: Comments; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public."Comments" (
    id integer NOT NULL,
    "commentedOnResource" integer,
    "threadID" integer,
    title character varying(255) NOT NULL,
    body character varying(255) NOT NULL,
    "createdBy" integer,
    "createdAt" timestamp with time zone NOT NULL
);


ALTER TABLE public."Comments" OWNER TO salcosser;

--
-- TOC entry 206 (class 1259 OID 43879)
-- Name: Comments_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."Comments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Comments_id_seq" OWNER TO salcosser;

--
-- TOC entry 3205 (class 0 OID 0)
-- Dependencies: 206
-- Name: Comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."Comments_id_seq" OWNED BY public."Comments".id;


--
-- TOC entry 217 (class 1259 OID 44008)
-- Name: ai_correlation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_correlation (
    taga character varying NOT NULL,
    tagb character varying NOT NULL,
    correlation double precision NOT NULL
);


ALTER TABLE public.ai_correlation OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 51892)
-- Name: assignmentresources; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.assignmentresources (
    "ResourceId" integer NOT NULL,
    "AssignmentId" integer NOT NULL
);


ALTER TABLE public.assignmentresources OWNER TO salcosser;

--
-- TOC entry 220 (class 1259 OID 51778)
-- Name: assignments; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.assignments (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description character varying(255) NOT NULL,
    creatorid integer,
    opendate timestamp with time zone NOT NULL,
    duedate timestamp with time zone NOT NULL,
    closedate timestamp with time zone NOT NULL,
    status character varying(255) NOT NULL,
    grade character varying(255),
    mutable boolean NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "LessonId" integer
);


ALTER TABLE public.assignments OWNER TO salcosser;

--
-- TOC entry 219 (class 1259 OID 51776)
-- Name: assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assignments_id_seq OWNER TO salcosser;

--
-- TOC entry 3206 (class 0 OID 0)
-- Dependencies: 219
-- Name: assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.assignments_id_seq OWNED BY public.assignments.id;


--
-- TOC entry 235 (class 1259 OID 51940)
-- Name: fgseq1; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.fgseq1
    START WITH 11
    INCREMENT BY 1
    MINVALUE 11
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fgseq1 OWNER TO salcosser;

--
-- TOC entry 218 (class 1259 OID 44016)
-- Name: favoritegroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favoritegroup (
    id integer DEFAULT nextval('public.fgseq1'::regclass) NOT NULL,
    groupid integer NOT NULL,
    userid integer NOT NULL
);


ALTER TABLE public.favoritegroup OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 51943)
-- Name: frseq1; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.frseq1
    START WITH 4
    INCREMENT BY 1
    MINVALUE 4
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.frseq1 OWNER TO salcosser;

--
-- TOC entry 228 (class 1259 OID 51860)
-- Name: favoriteresource; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.favoriteresource (
    id integer DEFAULT nextval('public.frseq1'::regclass) NOT NULL,
    resourceid integer NOT NULL,
    userid integer NOT NULL
);


ALTER TABLE public.favoriteresource OWNER TO salcosser;

--
-- TOC entry 227 (class 1259 OID 51858)
-- Name: favoriteresource_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.favoriteresource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favoriteresource_id_seq OWNER TO salcosser;

--
-- TOC entry 3207 (class 0 OID 0)
-- Dependencies: 227
-- Name: favoriteresource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.favoriteresource_id_seq OWNED BY public.favoriteresource.id;


--
-- TOC entry 234 (class 1259 OID 51937)
-- Name: fgseq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.fgseq
    START WITH 0
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fgseq OWNER TO salcosser;

--
-- TOC entry 230 (class 1259 OID 51878)
-- Name: file; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.file (
    id integer NOT NULL,
    uuid character varying(255) NOT NULL,
    uri character varying(255) NOT NULL,
    filename character varying(255) NOT NULL,
    filetype character varying(255) NOT NULL,
    dateupload timestamp with time zone,
    userid integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.file OWNER TO salcosser;

--
-- TOC entry 229 (class 1259 OID 51876)
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.file_id_seq OWNER TO salcosser;

--
-- TOC entry 3208 (class 0 OID 0)
-- Dependencies: 229
-- Name: file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.file_id_seq OWNED BY public.file.id;


--
-- TOC entry 209 (class 1259 OID 43915)
-- Name: friends; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.friends (
    "friendRequestid" integer NOT NULL,
    requesterid integer NOT NULL,
    addresseeid integer NOT NULL,
    status public.enum_friends_status DEFAULT 'p'::public.enum_friends_status
);


ALTER TABLE public.friends OWNER TO salcosser;

--
-- TOC entry 208 (class 1259 OID 43913)
-- Name: friends_friendRequestid_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."friends_friendRequestid_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."friends_friendRequestid_seq" OWNER TO salcosser;

--
-- TOC entry 3209 (class 0 OID 0)
-- Dependencies: 208
-- Name: friends_friendRequestid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."friends_friendRequestid_seq" OWNED BY public.friends."friendRequestid";


--
-- TOC entry 215 (class 1259 OID 43987)
-- Name: groupresources; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.groupresources (
    "ResourceId" integer NOT NULL,
    "GroupId" integer NOT NULL
);


ALTER TABLE public.groupresources OWNER TO salcosser;

--
-- TOC entry 203 (class 1259 OID 43843)
-- Name: groups; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.groups (
    id integer NOT NULL,
    groupname character varying(255) NOT NULL,
    groupdescription character varying(255) NOT NULL,
    resourceapi character varying(255) DEFAULT NULL::character varying,
    datetimeadd timestamp with time zone,
    datetimeremove timestamp with time zone,
    createdby integer
);


ALTER TABLE public.groups OWNER TO salcosser;

--
-- TOC entry 202 (class 1259 OID 43841)
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO salcosser;

--
-- TOC entry 3210 (class 0 OID 0)
-- Dependencies: 202
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.groups_id_seq OWNED BY public.groups.id;


--
-- TOC entry 233 (class 1259 OID 51922)
-- Name: lessonassignments; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.lessonassignments (
    "AssignmentId" integer NOT NULL,
    "LessonId" integer NOT NULL
);


ALTER TABLE public.lessonassignments OWNER TO salcosser;

--
-- TOC entry 232 (class 1259 OID 51907)
-- Name: lessonresources; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.lessonresources (
    "ResourceId" integer NOT NULL,
    "LessonId" integer NOT NULL
);


ALTER TABLE public.lessonresources OWNER TO salcosser;

--
-- TOC entry 222 (class 1259 OID 51794)
-- Name: lessons; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description character varying(255) NOT NULL,
    creatorid integer,
    mutable boolean NOT NULL,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.lessons OWNER TO salcosser;

--
-- TOC entry 221 (class 1259 OID 51792)
-- Name: lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lessons_id_seq OWNER TO salcosser;

--
-- TOC entry 3211 (class 0 OID 0)
-- Dependencies: 221
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- TOC entry 205 (class 1259 OID 43860)
-- Name: resources; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.resources (
    id integer NOT NULL,
    type character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    description character varying(255),
    link character varying(255),
    uri character varying(255),
    "fileName" character varying(255),
    mutable boolean NOT NULL,
    creatorid integer,
    "createdAt" timestamp with time zone NOT NULL,
    "updatedAt" timestamp with time zone NOT NULL,
    "GroupId" integer,
    "AssignmentId" integer,
    "LessonId" integer
);


ALTER TABLE public.resources OWNER TO salcosser;

--
-- TOC entry 204 (class 1259 OID 43858)
-- Name: resources_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.resources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.resources_id_seq OWNER TO salcosser;

--
-- TOC entry 3212 (class 0 OID 0)
-- Dependencies: 204
-- Name: resources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.resources_id_seq OWNED BY public.resources.id;


--
-- TOC entry 216 (class 1259 OID 44002)
-- Name: resourcetags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resourcetags (
    resourceid bigint NOT NULL,
    tags character varying NOT NULL
);


ALTER TABLE public.resourcetags OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 51810)
-- Name: shareassignments; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.shareassignments (
    "SharedID" integer NOT NULL,
    "AssignmentId" integer NOT NULL,
    "Sharedby" integer NOT NULL,
    "UserId" integer NOT NULL
);


ALTER TABLE public.shareassignments OWNER TO salcosser;

--
-- TOC entry 223 (class 1259 OID 51808)
-- Name: shareassignments_SharedID_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."shareassignments_SharedID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."shareassignments_SharedID_seq" OWNER TO salcosser;

--
-- TOC entry 3213 (class 0 OID 0)
-- Dependencies: 223
-- Name: shareassignments_SharedID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."shareassignments_SharedID_seq" OWNED BY public.shareassignments."SharedID";


--
-- TOC entry 211 (class 1259 OID 43934)
-- Name: sharegroup; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.sharegroup (
    "SharedID" integer NOT NULL,
    "GroupId" integer NOT NULL,
    "Sharedby" integer NOT NULL,
    "UserId" integer NOT NULL
);


ALTER TABLE public.sharegroup OWNER TO salcosser;

--
-- TOC entry 210 (class 1259 OID 43932)
-- Name: sharegroup_SharedID_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."sharegroup_SharedID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."sharegroup_SharedID_seq" OWNER TO salcosser;

--
-- TOC entry 3214 (class 0 OID 0)
-- Dependencies: 210
-- Name: sharegroup_SharedID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."sharegroup_SharedID_seq" OWNED BY public.sharegroup."SharedID";


--
-- TOC entry 226 (class 1259 OID 51835)
-- Name: sharelessons; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.sharelessons (
    "SharedID" integer NOT NULL,
    "LessonId" integer NOT NULL,
    "Sharedby" integer NOT NULL,
    "UserId" integer NOT NULL
);


ALTER TABLE public.sharelessons OWNER TO salcosser;

--
-- TOC entry 225 (class 1259 OID 51833)
-- Name: sharelessons_SharedID_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."sharelessons_SharedID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."sharelessons_SharedID_seq" OWNER TO salcosser;

--
-- TOC entry 3215 (class 0 OID 0)
-- Dependencies: 225
-- Name: sharelessons_SharedID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."sharelessons_SharedID_seq" OWNED BY public.sharelessons."SharedID";


--
-- TOC entry 213 (class 1259 OID 43959)
-- Name: shareresource; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.shareresource (
    "ShareResourceId" integer NOT NULL,
    "ResourceId" integer NOT NULL,
    "Sharedby" integer NOT NULL,
    "UserId" integer NOT NULL
);


ALTER TABLE public.shareresource OWNER TO salcosser;

--
-- TOC entry 212 (class 1259 OID 43957)
-- Name: shareresource_ShareResourceId_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public."shareresource_ShareResourceId_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."shareresource_ShareResourceId_seq" OWNER TO salcosser;

--
-- TOC entry 3216 (class 0 OID 0)
-- Dependencies: 212
-- Name: shareresource_ShareResourceId_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public."shareresource_ShareResourceId_seq" OWNED BY public.shareresource."ShareResourceId";


--
-- TOC entry 214 (class 1259 OID 43982)
-- Name: tags; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    tag character varying(255) NOT NULL,
    createdate timestamp with time zone NOT NULL
);


ALTER TABLE public.tags OWNER TO salcosser;

--
-- TOC entry 201 (class 1259 OID 43832)
-- Name: users; Type: TABLE; Schema: public; Owner: salcosser
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    hashpw character varying(255),
    firstname character varying(255) NOT NULL,
    lastname character varying(255) NOT NULL,
    country character varying(255),
    city character varying(255),
    phonenum character varying(255),
    email character varying(255)
);


ALTER TABLE public.users OWNER TO salcosser;

--
-- TOC entry 200 (class 1259 OID 43830)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: salcosser
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO salcosser;

--
-- TOC entry 3217 (class 0 OID 0)
-- Dependencies: 200
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: salcosser
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 2976 (class 2604 OID 43884)
-- Name: Comments id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public."Comments" ALTER COLUMN id SET DEFAULT nextval('public."Comments_id_seq"'::regclass);


--
-- TOC entry 2982 (class 2604 OID 51781)
-- Name: assignments id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignments ALTER COLUMN id SET DEFAULT nextval('public.assignments_id_seq'::regclass);


--
-- TOC entry 2987 (class 2604 OID 51881)
-- Name: file id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.file ALTER COLUMN id SET DEFAULT nextval('public.file_id_seq'::regclass);


--
-- TOC entry 2977 (class 2604 OID 43918)
-- Name: friends friendRequestid; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.friends ALTER COLUMN "friendRequestid" SET DEFAULT nextval('public."friends_friendRequestid_seq"'::regclass);


--
-- TOC entry 2973 (class 2604 OID 43846)
-- Name: groups id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groups ALTER COLUMN id SET DEFAULT nextval('public.groups_id_seq'::regclass);


--
-- TOC entry 2983 (class 2604 OID 51797)
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- TOC entry 2975 (class 2604 OID 43863)
-- Name: resources id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources ALTER COLUMN id SET DEFAULT nextval('public.resources_id_seq'::regclass);


--
-- TOC entry 2984 (class 2604 OID 51813)
-- Name: shareassignments SharedID; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments ALTER COLUMN "SharedID" SET DEFAULT nextval('public."shareassignments_SharedID_seq"'::regclass);


--
-- TOC entry 2979 (class 2604 OID 43937)
-- Name: sharegroup SharedID; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup ALTER COLUMN "SharedID" SET DEFAULT nextval('public."sharegroup_SharedID_seq"'::regclass);


--
-- TOC entry 2985 (class 2604 OID 51838)
-- Name: sharelessons SharedID; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons ALTER COLUMN "SharedID" SET DEFAULT nextval('public."sharelessons_SharedID_seq"'::regclass);


--
-- TOC entry 2980 (class 2604 OID 43962)
-- Name: shareresource ShareResourceId; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource ALTER COLUMN "ShareResourceId" SET DEFAULT nextval('public."shareresource_ShareResourceId_seq"'::regclass);


--
-- TOC entry 2972 (class 2604 OID 43835)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 2995 (class 2606 OID 43889)
-- Name: Comments Comments_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public."Comments"
    ADD CONSTRAINT "Comments_pkey" PRIMARY KEY (id);


--
-- TOC entry 3029 (class 2606 OID 51896)
-- Name: assignmentresources assignmentresources_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignmentresources
    ADD CONSTRAINT assignmentresources_pkey PRIMARY KEY ("ResourceId", "AssignmentId");


--
-- TOC entry 3013 (class 2606 OID 51786)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 3011 (class 2606 OID 44020)
-- Name: favoritegroup favoritegroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favoritegroup
    ADD CONSTRAINT favoritegroup_pkey PRIMARY KEY (id);


--
-- TOC entry 3025 (class 2606 OID 51865)
-- Name: favoriteresource favoriteresource_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.favoriteresource
    ADD CONSTRAINT favoriteresource_pkey PRIMARY KEY (id);


--
-- TOC entry 3027 (class 2606 OID 51886)
-- Name: file file_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_pkey PRIMARY KEY (uuid);


--
-- TOC entry 2997 (class 2606 OID 43921)
-- Name: friends friends_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_pkey PRIMARY KEY ("friendRequestid");


--
-- TOC entry 3009 (class 2606 OID 43991)
-- Name: groupresources groupresources_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groupresources
    ADD CONSTRAINT groupresources_pkey PRIMARY KEY ("ResourceId", "GroupId");


--
-- TOC entry 2991 (class 2606 OID 43852)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- TOC entry 3033 (class 2606 OID 51926)
-- Name: lessonassignments lessonassignments_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonassignments
    ADD CONSTRAINT lessonassignments_pkey PRIMARY KEY ("AssignmentId", "LessonId");


--
-- TOC entry 3031 (class 2606 OID 51911)
-- Name: lessonresources lessonresources_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonresources
    ADD CONSTRAINT lessonresources_pkey PRIMARY KEY ("ResourceId", "LessonId");


--
-- TOC entry 3015 (class 2606 OID 51802)
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- TOC entry 2993 (class 2606 OID 43868)
-- Name: resources resources_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT resources_pkey PRIMARY KEY (id);


--
-- TOC entry 3017 (class 2606 OID 51817)
-- Name: shareassignments shareassignments_AssignmentId_UserId_key; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments
    ADD CONSTRAINT "shareassignments_AssignmentId_UserId_key" UNIQUE ("AssignmentId", "UserId");


--
-- TOC entry 3019 (class 2606 OID 51815)
-- Name: shareassignments shareassignments_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments
    ADD CONSTRAINT shareassignments_pkey PRIMARY KEY ("SharedID");


--
-- TOC entry 2999 (class 2606 OID 43941)
-- Name: sharegroup sharegroup_GroupId_UserId_key; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup
    ADD CONSTRAINT "sharegroup_GroupId_UserId_key" UNIQUE ("GroupId", "UserId");


--
-- TOC entry 3001 (class 2606 OID 43939)
-- Name: sharegroup sharegroup_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup
    ADD CONSTRAINT sharegroup_pkey PRIMARY KEY ("SharedID");


--
-- TOC entry 3021 (class 2606 OID 51842)
-- Name: sharelessons sharelessons_LessonId_UserId_key; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons
    ADD CONSTRAINT "sharelessons_LessonId_UserId_key" UNIQUE ("LessonId", "UserId");


--
-- TOC entry 3023 (class 2606 OID 51840)
-- Name: sharelessons sharelessons_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons
    ADD CONSTRAINT sharelessons_pkey PRIMARY KEY ("SharedID");


--
-- TOC entry 3003 (class 2606 OID 43966)
-- Name: shareresource shareresource_ResourceId_UserId_key; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource
    ADD CONSTRAINT "shareresource_ResourceId_UserId_key" UNIQUE ("ResourceId", "UserId");


--
-- TOC entry 3005 (class 2606 OID 43964)
-- Name: shareresource shareresource_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource
    ADD CONSTRAINT shareresource_pkey PRIMARY KEY ("ShareResourceId");


--
-- TOC entry 3007 (class 2606 OID 43986)
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- TOC entry 2989 (class 2606 OID 43840)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3039 (class 2606 OID 43890)
-- Name: Comments Comments_commentedOnResource_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public."Comments"
    ADD CONSTRAINT "Comments_commentedOnResource_fkey" FOREIGN KEY ("commentedOnResource") REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3041 (class 2606 OID 43900)
-- Name: Comments Comments_createdBy_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public."Comments"
    ADD CONSTRAINT "Comments_createdBy_fkey" FOREIGN KEY ("createdBy") REFERENCES public.users(id);


--
-- TOC entry 3040 (class 2606 OID 43895)
-- Name: Comments Comments_threadID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public."Comments"
    ADD CONSTRAINT "Comments_threadID_fkey" FOREIGN KEY ("threadID") REFERENCES public."Comments"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3065 (class 2606 OID 51902)
-- Name: assignmentresources assignmentresources_AssignmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignmentresources
    ADD CONSTRAINT "assignmentresources_AssignmentId_fkey" FOREIGN KEY ("AssignmentId") REFERENCES public.assignments(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3064 (class 2606 OID 51897)
-- Name: assignmentresources assignmentresources_ResourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignmentresources
    ADD CONSTRAINT "assignmentresources_ResourceId_fkey" FOREIGN KEY ("ResourceId") REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3053 (class 2606 OID 51961)
-- Name: assignments assignments_LessonId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT "assignments_LessonId_fkey" FOREIGN KEY ("LessonId") REFERENCES public.lessons(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3052 (class 2606 OID 51787)
-- Name: assignments assignments_creatorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_creatorid_fkey FOREIGN KEY (creatorid) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3061 (class 2606 OID 51866)
-- Name: favoriteresource favoriteresource_resourceid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.favoriteresource
    ADD CONSTRAINT favoriteresource_resourceid_fkey FOREIGN KEY (resourceid) REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3062 (class 2606 OID 51871)
-- Name: favoriteresource favoriteresource_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.favoriteresource
    ADD CONSTRAINT favoriteresource_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3063 (class 2606 OID 51887)
-- Name: file file_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(id);


--
-- TOC entry 3043 (class 2606 OID 43927)
-- Name: friends friends_addresseeid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_addresseeid_fkey FOREIGN KEY (addresseeid) REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3042 (class 2606 OID 43922)
-- Name: friends friends_requesterid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.friends
    ADD CONSTRAINT friends_requesterid_fkey FOREIGN KEY (requesterid) REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3051 (class 2606 OID 43997)
-- Name: groupresources groupresources_GroupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groupresources
    ADD CONSTRAINT "groupresources_GroupId_fkey" FOREIGN KEY ("GroupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3050 (class 2606 OID 43992)
-- Name: groupresources groupresources_ResourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groupresources
    ADD CONSTRAINT "groupresources_ResourceId_fkey" FOREIGN KEY ("ResourceId") REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3034 (class 2606 OID 43853)
-- Name: groups groups_createdby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_createdby_fkey FOREIGN KEY (createdby) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3068 (class 2606 OID 51927)
-- Name: lessonassignments lessonassignments_AssignmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonassignments
    ADD CONSTRAINT "lessonassignments_AssignmentId_fkey" FOREIGN KEY ("AssignmentId") REFERENCES public.assignments(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3069 (class 2606 OID 51932)
-- Name: lessonassignments lessonassignments_LessonId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonassignments
    ADD CONSTRAINT "lessonassignments_LessonId_fkey" FOREIGN KEY ("LessonId") REFERENCES public.lessons(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3067 (class 2606 OID 51917)
-- Name: lessonresources lessonresources_LessonId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonresources
    ADD CONSTRAINT "lessonresources_LessonId_fkey" FOREIGN KEY ("LessonId") REFERENCES public.lessons(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3066 (class 2606 OID 51912)
-- Name: lessonresources lessonresources_ResourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessonresources
    ADD CONSTRAINT "lessonresources_ResourceId_fkey" FOREIGN KEY ("ResourceId") REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3054 (class 2606 OID 51803)
-- Name: lessons lessons_creatorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_creatorid_fkey FOREIGN KEY (creatorid) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3037 (class 2606 OID 51951)
-- Name: resources resources_AssignmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT "resources_AssignmentId_fkey" FOREIGN KEY ("AssignmentId") REFERENCES public.assignments(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3036 (class 2606 OID 43874)
-- Name: resources resources_GroupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT "resources_GroupId_fkey" FOREIGN KEY ("GroupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3038 (class 2606 OID 51956)
-- Name: resources resources_LessonId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT "resources_LessonId_fkey" FOREIGN KEY ("LessonId") REFERENCES public.lessons(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3035 (class 2606 OID 43869)
-- Name: resources resources_creatorid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.resources
    ADD CONSTRAINT resources_creatorid_fkey FOREIGN KEY (creatorid) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- TOC entry 3055 (class 2606 OID 51818)
-- Name: shareassignments shareassignments_AssignmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments
    ADD CONSTRAINT "shareassignments_AssignmentId_fkey" FOREIGN KEY ("AssignmentId") REFERENCES public.assignments(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3056 (class 2606 OID 51823)
-- Name: shareassignments shareassignments_Sharedby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments
    ADD CONSTRAINT "shareassignments_Sharedby_fkey" FOREIGN KEY ("Sharedby") REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3057 (class 2606 OID 51828)
-- Name: shareassignments shareassignments_UserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareassignments
    ADD CONSTRAINT "shareassignments_UserId_fkey" FOREIGN KEY ("UserId") REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3044 (class 2606 OID 43942)
-- Name: sharegroup sharegroup_GroupId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup
    ADD CONSTRAINT "sharegroup_GroupId_fkey" FOREIGN KEY ("GroupId") REFERENCES public.groups(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3045 (class 2606 OID 43947)
-- Name: sharegroup sharegroup_Sharedby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup
    ADD CONSTRAINT "sharegroup_Sharedby_fkey" FOREIGN KEY ("Sharedby") REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3046 (class 2606 OID 43952)
-- Name: sharegroup sharegroup_UserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharegroup
    ADD CONSTRAINT "sharegroup_UserId_fkey" FOREIGN KEY ("UserId") REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3058 (class 2606 OID 51843)
-- Name: sharelessons sharelessons_LessonId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons
    ADD CONSTRAINT "sharelessons_LessonId_fkey" FOREIGN KEY ("LessonId") REFERENCES public.lessons(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3059 (class 2606 OID 51848)
-- Name: sharelessons sharelessons_Sharedby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons
    ADD CONSTRAINT "sharelessons_Sharedby_fkey" FOREIGN KEY ("Sharedby") REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3060 (class 2606 OID 51853)
-- Name: sharelessons sharelessons_UserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.sharelessons
    ADD CONSTRAINT "sharelessons_UserId_fkey" FOREIGN KEY ("UserId") REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3047 (class 2606 OID 43967)
-- Name: shareresource shareresource_ResourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource
    ADD CONSTRAINT "shareresource_ResourceId_fkey" FOREIGN KEY ("ResourceId") REFERENCES public.resources(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3048 (class 2606 OID 43972)
-- Name: shareresource shareresource_Sharedby_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource
    ADD CONSTRAINT "shareresource_Sharedby_fkey" FOREIGN KEY ("Sharedby") REFERENCES public.users(id) ON UPDATE CASCADE;


--
-- TOC entry 3049 (class 2606 OID 43977)
-- Name: shareresource shareresource_UserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: salcosser
--

ALTER TABLE ONLY public.shareresource
    ADD CONSTRAINT "shareresource_UserId_fkey" FOREIGN KEY ("UserId") REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


-- Completed on 2021-12-07 16:52:14

--
-- PostgreSQL database dump complete
--

