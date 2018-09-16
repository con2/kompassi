--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Debian 10.4-2.pgdg90+1)
-- Dumped by pg_dump version 10.4 (Debian 10.4-2.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: access_accessorganizationmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_accessorganizationmeta (
    organization_id integer NOT NULL,
    admin_group_id integer NOT NULL
);


--
-- Name: access_emailalias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_emailalias (
    id integer NOT NULL,
    account_name character varying(255) NOT NULL,
    email_address character varying(511) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    domain_id integer NOT NULL,
    group_grant_id integer,
    person_id integer NOT NULL,
    type_id integer NOT NULL
);


--
-- Name: access_emailalias_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_emailalias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_emailalias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_emailalias_id_seq OWNED BY public.access_emailalias.id;


--
-- Name: access_emailaliasdomain; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_emailaliasdomain (
    id integer NOT NULL,
    domain_name character varying(255) NOT NULL,
    organization_id integer NOT NULL,
    has_internal_aliases boolean NOT NULL
);


--
-- Name: access_emailaliasdomain_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_emailaliasdomain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_emailaliasdomain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_emailaliasdomain_id_seq OWNED BY public.access_emailaliasdomain.id;


--
-- Name: access_emailaliastype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_emailaliastype (
    id integer NOT NULL,
    metavar character varying(255) NOT NULL,
    account_name_code character varying(255) NOT NULL,
    domain_id integer NOT NULL,
    priority integer NOT NULL
);


--
-- Name: access_emailaliastype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_emailaliastype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_emailaliastype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_emailaliastype_id_seq OWNED BY public.access_emailaliastype.id;


--
-- Name: access_grantedprivilege; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_grantedprivilege (
    id integer NOT NULL,
    granted_at timestamp with time zone NOT NULL,
    person_id integer NOT NULL,
    privilege_id integer NOT NULL,
    state character varying(8) NOT NULL
);


--
-- Name: access_grantedprivilege_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_grantedprivilege_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_grantedprivilege_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_grantedprivilege_id_seq OWNED BY public.access_grantedprivilege.id;


--
-- Name: access_groupemailaliasgrant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_groupemailaliasgrant (
    id integer NOT NULL,
    group_id integer NOT NULL,
    type_id integer NOT NULL,
    active_until timestamp with time zone
);


--
-- Name: access_groupemailaliasgrant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_groupemailaliasgrant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_groupemailaliasgrant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_groupemailaliasgrant_id_seq OWNED BY public.access_groupemailaliasgrant.id;


--
-- Name: access_groupprivilege; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_groupprivilege (
    id integer NOT NULL,
    event_id integer,
    group_id integer NOT NULL,
    privilege_id integer NOT NULL
);


--
-- Name: access_groupprivilege_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_groupprivilege_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_groupprivilege_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_groupprivilege_id_seq OWNED BY public.access_groupprivilege.id;


--
-- Name: access_internalemailalias; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_internalemailalias (
    id integer NOT NULL,
    account_name character varying(255) NOT NULL,
    target_emails character varying(1023) NOT NULL,
    email_address character varying(511) NOT NULL,
    app_label character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    domain_id integer NOT NULL,
    event_id integer
);


--
-- Name: access_internalemailalias_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_internalemailalias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_internalemailalias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_internalemailalias_id_seq OWNED BY public.access_internalemailalias.id;


--
-- Name: access_privilege; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_privilege (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(256) NOT NULL,
    description text NOT NULL,
    request_success_message text NOT NULL,
    grant_code character varying(256) NOT NULL,
    disclaimers text NOT NULL
);


--
-- Name: access_privilege_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_privilege_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_privilege_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_privilege_id_seq OWNED BY public.access_privilege.id;


--
-- Name: access_slackaccess; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_slackaccess (
    id integer NOT NULL,
    team_name character varying(255) NOT NULL,
    api_token character varying(255) NOT NULL,
    privilege_id integer NOT NULL
);


--
-- Name: access_slackaccess_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_slackaccess_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_slackaccess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_slackaccess_id_seq OWNED BY public.access_slackaccess.id;


--
-- Name: access_smtppassword; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_smtppassword (
    id integer NOT NULL,
    password_hash character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    person_id integer NOT NULL,
    smtp_server_id integer NOT NULL
);


--
-- Name: access_smtppassword_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_smtppassword_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_smtppassword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_smtppassword_id_seq OWNED BY public.access_smtppassword.id;


--
-- Name: access_smtpserver; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_smtpserver (
    id integer NOT NULL,
    hostname character varying(255) NOT NULL,
    crypto character varying(5) NOT NULL,
    port integer NOT NULL
);


--
-- Name: access_smtpserver_domains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.access_smtpserver_domains (
    id integer NOT NULL,
    smtpserver_id integer NOT NULL,
    emailaliasdomain_id integer NOT NULL
);


--
-- Name: access_smtpserver_domains_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_smtpserver_domains_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_smtpserver_domains_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_smtpserver_domains_id_seq OWNED BY public.access_smtpserver_domains.id;


--
-- Name: access_smtpserver_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.access_smtpserver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: access_smtpserver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.access_smtpserver_id_seq OWNED BY public.access_smtpserver.id;


--
-- Name: aicon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    need_lodging boolean NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    email_alias character varying(32) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: aicon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: aicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aicon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: aicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aicon2016_signupextra_special_diet_id_seq OWNED BY public.aicon2016_signupextra_special_diet.id;


--
-- Name: aicon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: aicon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aicon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: aicon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aicon2016_specialdiet_id_seq OWNED BY public.aicon2016_specialdiet.id;


--
-- Name: aicon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2018_signupextra (
    signup_id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    need_lodging boolean NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    email_alias character varying(32) NOT NULL
);


--
-- Name: aicon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: aicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aicon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: aicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aicon2018_signupextra_special_diet_id_seq OWNED BY public.aicon2018_signupextra_special_diet.id;


--
-- Name: aicon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.aicon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: aicon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.aicon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: aicon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.aicon2018_specialdiet_id_seq OWNED BY public.aicon2018_specialdiet.id;


--
-- Name: animecon2015_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2015_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: animecon2015_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2015_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2015_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2015_night_id_seq OWNED BY public.animecon2015_night.id;


--
-- Name: animecon2015_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2015_signupextra (
    signup_id integer NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    personal_identification_number character varying(12) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: animecon2015_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2015_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: animecon2015_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2015_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2015_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2015_signupextra_lodging_needs_id_seq OWNED BY public.animecon2015_signupextra_lodging_needs.id;


--
-- Name: animecon2015_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2015_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: animecon2015_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2015_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2015_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2015_signupextra_special_diet_id_seq OWNED BY public.animecon2015_signupextra_special_diet.id;


--
-- Name: animecon2015_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2015_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: animecon2015_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2015_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2015_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2015_specialdiet_id_seq OWNED BY public.animecon2015_specialdiet.id;


--
-- Name: animecon2016_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2016_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: animecon2016_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2016_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2016_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2016_night_id_seq OWNED BY public.animecon2016_night.id;


--
-- Name: animecon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2016_signupextra (
    signup_id integer NOT NULL,
    total_work character varying(15) NOT NULL,
    personal_identification_number character varying(12) NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: animecon2016_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2016_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: animecon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2016_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2016_signupextra_lodging_needs_id_seq OWNED BY public.animecon2016_signupextra_lodging_needs.id;


--
-- Name: animecon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: animecon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2016_signupextra_special_diet_id_seq OWNED BY public.animecon2016_signupextra_special_diet.id;


--
-- Name: animecon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.animecon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: animecon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.animecon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: animecon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.animecon2016_specialdiet_id_seq OWNED BY public.animecon2016_specialdiet.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: badges_badge; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.badges_badge (
    id integer NOT NULL,
    printed_separately_at timestamp with time zone,
    revoked_at timestamp with time zone,
    job_title character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    batch_id integer,
    person_id integer,
    personnel_class_id integer NOT NULL,
    first_name character varying(1023) NOT NULL,
    is_first_name_visible boolean NOT NULL,
    is_nick_visible boolean NOT NULL,
    is_surname_visible boolean NOT NULL,
    nick character varying(1023) NOT NULL,
    surname character varying(1023) NOT NULL,
    created_by_id integer,
    revoked_by_id integer,
    arrived_at timestamp with time zone,
    notes text NOT NULL
);


--
-- Name: badges_badge_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.badges_badge_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: badges_badge_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.badges_badge_id_seq OWNED BY public.badges_badge.id;


--
-- Name: badges_badgeseventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.badges_badgeseventmeta (
    event_id integer NOT NULL,
    admin_group_id integer NOT NULL,
    badge_layout character varying(4) NOT NULL,
    real_name_must_be_visible boolean NOT NULL,
    is_using_fuzzy_reissuance_hack boolean NOT NULL
);


--
-- Name: badges_batch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.badges_batch (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    printed_at timestamp with time zone,
    event_id integer NOT NULL,
    personnel_class_id integer
);


--
-- Name: badges_batch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.badges_batch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: badges_batch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.badges_batch_id_seq OWNED BY public.badges_batch.id;


--
-- Name: core_carouselslide; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_carouselslide (
    id integer NOT NULL,
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    href character varying(512) NOT NULL,
    title character varying(512) NOT NULL,
    image_file character varying(100) NOT NULL,
    image_credit character varying(512) NOT NULL,
    target character varying(6) NOT NULL,
    "order" integer NOT NULL
);


--
-- Name: core_carouselslide_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_carouselslide_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_carouselslide_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_carouselslide_id_seq OWNED BY public.core_carouselslide.id;


--
-- Name: core_emailverificationtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_emailverificationtoken (
    id integer NOT NULL,
    code character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    state character varying(8) NOT NULL,
    email character varying(255) NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: core_emailverificationtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_emailverificationtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_emailverificationtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_emailverificationtoken_id_seq OWNED BY public.core_emailverificationtoken.id;


--
-- Name: core_event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_event (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    name character varying(63) NOT NULL,
    name_genitive character varying(63) NOT NULL,
    name_illative character varying(63) NOT NULL,
    name_inessive character varying(63) NOT NULL,
    description text NOT NULL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    homepage_url character varying(255) NOT NULL,
    public boolean NOT NULL,
    venue_id integer NOT NULL,
    logo_url character varying(255) NOT NULL,
    organization_id integer NOT NULL,
    panel_css_class character varying(255) NOT NULL,
    logo_file character varying(100) NOT NULL
);


--
-- Name: core_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_event_id_seq OWNED BY public.core_event.id;


--
-- Name: core_organization; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_organization (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    homepage_url character varying(255) NOT NULL,
    description text NOT NULL,
    logo_url character varying(255) NOT NULL,
    public boolean NOT NULL,
    muncipality character varying(127) NOT NULL,
    name_genitive character varying(255) NOT NULL
);


--
-- Name: core_organization_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_organization_id_seq OWNED BY public.core_organization.id;


--
-- Name: core_passwordresettoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_passwordresettoken (
    id integer NOT NULL,
    code character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    state character varying(8) NOT NULL,
    ip_address character varying(45) NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: core_passwordresettoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_passwordresettoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_passwordresettoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_passwordresettoken_id_seq OWNED BY public.core_passwordresettoken.id;


--
-- Name: core_person; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_person (
    id integer NOT NULL,
    first_name character varying(1023) NOT NULL,
    surname character varying(1023) NOT NULL,
    nick character varying(1023) NOT NULL,
    birth_date date,
    email character varying(255) NOT NULL,
    phone character varying(255) NOT NULL,
    may_send_info boolean NOT NULL,
    preferred_name_display_style character varying(31) NOT NULL,
    notes text NOT NULL,
    email_verified_at timestamp with time zone,
    user_id integer,
    muncipality character varying(127) NOT NULL,
    official_first_names character varying(1023) NOT NULL,
    allow_work_history_sharing boolean NOT NULL
);


--
-- Name: core_person_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_person_id_seq OWNED BY public.core_person.id;


--
-- Name: core_venue; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.core_venue (
    id integer NOT NULL,
    name character varying(63) NOT NULL,
    name_inessive character varying(63) NOT NULL
);


--
-- Name: core_venue_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.core_venue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: core_venue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.core_venue_id_seq OWNED BY public.core_venue.id;


--
-- Name: desucon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    desu_amount integer NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    special_diet_other text NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT desucon2016_signupextra_desu_amount_check CHECK ((desu_amount >= 0))
);


--
-- Name: desucon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: desucon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2016_signupextra_special_diet_id_seq OWNED BY public.desucon2016_signupextra_special_diet.id;


--
-- Name: desucon2016_signupextrav2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2016_signupextrav2 (
    id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    desu_amount integer NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT desucon2016_signupextrav2_desu_amount_check CHECK ((desu_amount >= 0))
);


--
-- Name: desucon2016_signupextrav2_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2016_signupextrav2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2016_signupextrav2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2016_signupextrav2_id_seq OWNED BY public.desucon2016_signupextrav2.id;


--
-- Name: desucon2016_signupextrav2_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2016_signupextrav2_special_diet (
    id integer NOT NULL,
    signupextrav2_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: desucon2016_signupextrav2_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2016_signupextrav2_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2016_signupextrav2_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2016_signupextrav2_special_diet_id_seq OWNED BY public.desucon2016_signupextrav2_special_diet.id;


--
-- Name: desucon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: desucon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2016_specialdiet_id_seq OWNED BY public.desucon2016_specialdiet.id;


--
-- Name: desucon2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: desucon2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2017_signupextra_id_seq OWNED BY public.desucon2017_signupextra.id;


--
-- Name: desucon2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: desucon2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2017_signupextra_special_diet_id_seq OWNED BY public.desucon2017_signupextra_special_diet.id;


--
-- Name: desucon2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: desucon2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2017_specialdiet_id_seq OWNED BY public.desucon2017_specialdiet.id;


--
-- Name: desucon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    afterparty_participation boolean NOT NULL
);


--
-- Name: desucon2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2018_signupextra_id_seq OWNED BY public.desucon2018_signupextra.id;


--
-- Name: desucon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: desucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2018_signupextra_special_diet_id_seq OWNED BY public.desucon2018_signupextra_special_diet.id;


--
-- Name: desucon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: desucon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2018_specialdiet_id_seq OWNED BY public.desucon2018_specialdiet.id;


--
-- Name: desucon2019_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2019_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    afterparty_participation boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: desucon2019_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2019_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2019_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2019_signupextra_id_seq OWNED BY public.desucon2019_signupextra.id;


--
-- Name: desucon2019_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2019_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: desucon2019_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2019_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2019_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2019_signupextra_special_diet_id_seq OWNED BY public.desucon2019_signupextra_special_diet.id;


--
-- Name: desucon2019_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desucon2019_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: desucon2019_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desucon2019_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desucon2019_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desucon2019_specialdiet_id_seq OWNED BY public.desucon2019_specialdiet.id;


--
-- Name: desuprofile_integration_confirmationcode; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desuprofile_integration_confirmationcode (
    id integer NOT NULL,
    code character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    state character varying(8) NOT NULL,
    desuprofile_id integer NOT NULL,
    person_id integer NOT NULL,
    next_url character varying(1023) NOT NULL,
    desuprofile_username character varying(30) NOT NULL
);


--
-- Name: desuprofile_integration_confirmationcode_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.desuprofile_integration_confirmationcode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: desuprofile_integration_confirmationcode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.desuprofile_integration_confirmationcode_id_seq OWNED BY public.desuprofile_integration_confirmationcode.id;


--
-- Name: desuprofile_integration_connection; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.desuprofile_integration_connection (
    id integer NOT NULL,
    user_id integer NOT NULL,
    desuprofile_username character varying(30) NOT NULL
);


--
-- Name: directory_directoryaccessgroup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.directory_directoryaccessgroup (
    id integer NOT NULL,
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    group_id integer NOT NULL,
    organization_id integer NOT NULL
);


--
-- Name: directory_directoryaccessgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.directory_directoryaccessgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: directory_directoryaccessgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.directory_directoryaccessgroup_id_seq OWNED BY public.directory_directoryaccessgroup.id;


--
-- Name: directory_directoryorganizationmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.directory_directoryorganizationmeta (
    organization_id integer NOT NULL
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;


--
-- Name: enrollment_conconpart; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_conconpart (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: enrollment_conconpart_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_conconpart_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enrollment_conconpart_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_conconpart_id_seq OWNED BY public.enrollment_conconpart.id;


--
-- Name: enrollment_enrollment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_enrollment (
    id integer NOT NULL,
    special_diet_other text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    concon_event_affiliation character varying(512) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    is_public boolean,
    state character varying(9) NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


--
-- Name: enrollment_enrollment_concon_parts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_enrollment_concon_parts (
    id integer NOT NULL,
    enrollment_id integer NOT NULL,
    conconpart_id integer NOT NULL
);


--
-- Name: enrollment_enrollment_concon_parts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_enrollment_concon_parts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enrollment_enrollment_concon_parts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_enrollment_concon_parts_id_seq OWNED BY public.enrollment_enrollment_concon_parts.id;


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_enrollment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_enrollment_id_seq OWNED BY public.enrollment_enrollment.id;


--
-- Name: enrollment_enrollment_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_enrollment_special_diet (
    id integer NOT NULL,
    enrollment_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: enrollment_enrollment_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_enrollment_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enrollment_enrollment_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_enrollment_special_diet_id_seq OWNED BY public.enrollment_enrollment_special_diet.id;


--
-- Name: enrollment_enrollmenteventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_enrollmenteventmeta (
    event_id integer NOT NULL,
    form_class_path character varying(63) NOT NULL,
    enrollment_opens timestamp with time zone,
    enrollment_closes timestamp with time zone,
    admin_group_id integer NOT NULL,
    override_enrollment_form_message text NOT NULL,
    initial_state character varying(8) NOT NULL,
    is_participant_list_public boolean NOT NULL
);


--
-- Name: enrollment_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.enrollment_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: enrollment_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.enrollment_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: enrollment_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.enrollment_specialdiet_id_seq OWNED BY public.enrollment_specialdiet.id;


--
-- Name: event_log_entry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_log_entry (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    entry_type character varying(255) NOT NULL,
    created_by_id integer,
    feedback_message_id integer,
    event_id integer,
    event_survey_result_id integer,
    global_survey_result_id integer,
    context character varying(1024) NOT NULL,
    person_id integer,
    organization_id integer,
    search_term character varying(255) NOT NULL,
    ip_address character varying(48) NOT NULL
);


--
-- Name: event_log_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.event_log_entry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: event_log_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.event_log_entry_id_seq OWNED BY public.event_log_entry.id;


--
-- Name: event_log_subscription; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_log_subscription (
    id integer NOT NULL,
    entry_type character varying(255) NOT NULL,
    channel character varying(8) NOT NULL,
    active boolean NOT NULL,
    user_id integer NOT NULL,
    callback_code character varying(255) NOT NULL,
    event_filter_id integer,
    event_survey_filter_id integer
);


--
-- Name: event_log_subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.event_log_subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: event_log_subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.event_log_subscription_id_seq OWNED BY public.event_log_subscription.id;


--
-- Name: feedback_feedbackmessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.feedback_feedbackmessage (
    id integer NOT NULL,
    context character varying(1024) NOT NULL,
    author_ip_address character varying(48) NOT NULL,
    feedback text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    author_id integer
);


--
-- Name: feedback_feedbackmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.feedback_feedbackmessage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: feedback_feedbackmessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.feedback_feedbackmessage_id_seq OWNED BY public.feedback_feedbackmessage.id;


--
-- Name: finncon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    dead_dog boolean NOT NULL,
    shirt_size character varying(8),
    is_active boolean NOT NULL
);


--
-- Name: finncon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: finncon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.finncon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: finncon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.finncon2016_signupextra_special_diet_id_seq OWNED BY public.finncon2016_signupextra_special_diet.id;


--
-- Name: finncon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: finncon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.finncon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: finncon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.finncon2016_specialdiet_id_seq OWNED BY public.finncon2016_specialdiet.id;


--
-- Name: finncon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2018_signupextra (
    signup_id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    shirt_size character varying(8),
    dead_dog boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    language_skills text NOT NULL
);


--
-- Name: finncon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: finncon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.finncon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: finncon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.finncon2018_signupextra_special_diet_id_seq OWNED BY public.finncon2018_signupextra_special_diet.id;


--
-- Name: finncon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.finncon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: finncon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.finncon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: finncon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.finncon2018_specialdiet_id_seq OWNED BY public.finncon2018_specialdiet.id;


--
-- Name: frostbite2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    desu_amount integer NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT frostbite2016_signupextra_desu_amount_a3aa3252_check CHECK ((desu_amount >= 0))
);


--
-- Name: frostbite2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    desu_amount integer NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    CONSTRAINT frostbite2017_signupextra_desu_amount_check CHECK ((desu_amount >= 0))
);


--
-- Name: frostbite2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2017_signupextra_id_seq OWNED BY public.frostbite2017_signupextra.id;


--
-- Name: frostbite2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: frostbite2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2017_signupextra_special_diet_id_seq OWNED BY public.frostbite2017_signupextra_special_diet.id;


--
-- Name: frostbite2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: frostbite2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2017_specialdiet_id_seq OWNED BY public.frostbite2017_specialdiet.id;


--
-- Name: frostbite2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: frostbite2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2018_signupextra_id_seq OWNED BY public.frostbite2018_signupextra.id;


--
-- Name: frostbite2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: frostbite2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2018_signupextra_special_diet_id_seq OWNED BY public.frostbite2018_signupextra_special_diet.id;


--
-- Name: frostbite2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: frostbite2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2018_specialdiet_id_seq OWNED BY public.frostbite2018_specialdiet.id;


--
-- Name: frostbite2019_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2019_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    special_diet_other text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shirt_type character varying(8) NOT NULL,
    night_work boolean NOT NULL,
    afterparty_participation boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: frostbite2019_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2019_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2019_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2019_signupextra_id_seq OWNED BY public.frostbite2019_signupextra.id;


--
-- Name: frostbite2019_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2019_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: frostbite2019_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2019_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2019_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2019_signupextra_special_diet_id_seq OWNED BY public.frostbite2019_signupextra_special_diet.id;


--
-- Name: frostbite2019_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.frostbite2019_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: frostbite2019_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.frostbite2019_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: frostbite2019_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.frostbite2019_specialdiet_id_seq OWNED BY public.frostbite2019_specialdiet.id;


--
-- Name: hitpoint2015_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2015_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    construction boolean NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    night_work character varying(5) NOT NULL,
    shift_wishes text NOT NULL,
    need_lodging boolean NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: hitpoint2015_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2015_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: hitpoint2015_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hitpoint2015_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hitpoint2015_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hitpoint2015_signupextra_special_diet_id_seq OWNED BY public.hitpoint2015_signupextra_special_diet.id;


--
-- Name: hitpoint2015_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2015_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: hitpoint2015_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hitpoint2015_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hitpoint2015_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hitpoint2015_specialdiet_id_seq OWNED BY public.hitpoint2015_specialdiet.id;


--
-- Name: hitpoint2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2017_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    night_work character varying(5) NOT NULL,
    construction boolean NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    need_lodging boolean NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: hitpoint2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: hitpoint2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hitpoint2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hitpoint2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hitpoint2017_signupextra_special_diet_id_seq OWNED BY public.hitpoint2017_signupextra_special_diet.id;


--
-- Name: hitpoint2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: hitpoint2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hitpoint2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hitpoint2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hitpoint2017_specialdiet_id_seq OWNED BY public.hitpoint2017_specialdiet.id;


--
-- Name: hitpoint2017_timeslot; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hitpoint2017_timeslot (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: hitpoint2017_timeslot_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hitpoint2017_timeslot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hitpoint2017_timeslot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hitpoint2017_timeslot_id_seq OWNED BY public.hitpoint2017_timeslot.id;


--
-- Name: intra_intraeventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intra_intraeventmeta (
    event_id integer NOT NULL,
    admin_group_id integer NOT NULL,
    organizer_group_id integer NOT NULL
);


--
-- Name: intra_team; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intra_team (
    id integer NOT NULL,
    "order" integer NOT NULL,
    name character varying(256) NOT NULL,
    description text NOT NULL,
    slug character varying(255) NOT NULL,
    event_id integer NOT NULL,
    group_id integer NOT NULL,
    email character varying(255) NOT NULL
);


--
-- Name: intra_team_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.intra_team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: intra_team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.intra_team_id_seq OWNED BY public.intra_team.id;


--
-- Name: intra_teammember; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.intra_teammember (
    id integer NOT NULL,
    is_primary_team boolean NOT NULL,
    is_team_leader boolean NOT NULL,
    is_shown_internally boolean NOT NULL,
    is_shown_publicly boolean NOT NULL,
    is_group_member boolean NOT NULL,
    person_id integer NOT NULL,
    team_id integer NOT NULL,
    override_name_display_style character varying(22) NOT NULL,
    override_job_title character varying(63) NOT NULL
);


--
-- Name: intra_teammember_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.intra_teammember_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: intra_teammember_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.intra_teammember_id_seq OWNED BY public.intra_teammember.id;


--
-- Name: kawacon2016_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2016_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kawacon2016_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2016_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2016_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2016_night_id_seq OWNED BY public.kawacon2016_night.id;


--
-- Name: kawacon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2016_signupextra (
    signup_id integer NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: kawacon2016_signupextra_needs_lodging; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2016_signupextra_needs_lodging (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: kawacon2016_signupextra_needs_lodging_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2016_signupextra_needs_lodging_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2016_signupextra_needs_lodging_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2016_signupextra_needs_lodging_id_seq OWNED BY public.kawacon2016_signupextra_needs_lodging.id;


--
-- Name: kawacon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kawacon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2016_signupextra_special_diet_id_seq OWNED BY public.kawacon2016_signupextra_special_diet.id;


--
-- Name: kawacon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kawacon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2016_specialdiet_id_seq OWNED BY public.kawacon2016_specialdiet.id;


--
-- Name: kawacon2017_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kawacon2017_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_night_id_seq OWNED BY public.kawacon2017_night.id;


--
-- Name: kawacon2017_shift; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_shift (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kawacon2017_shift_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_shift_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_shift_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_shift_id_seq OWNED BY public.kawacon2017_shift.id;


--
-- Name: kawacon2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    afterparty character varying(3) NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    want_certificate boolean NOT NULL
);


--
-- Name: kawacon2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_signupextra_id_seq OWNED BY public.kawacon2017_signupextra.id;


--
-- Name: kawacon2017_signupextra_needs_lodging; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_signupextra_needs_lodging (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: kawacon2017_signupextra_needs_lodging_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_signupextra_needs_lodging_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_signupextra_needs_lodging_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_signupextra_needs_lodging_id_seq OWNED BY public.kawacon2017_signupextra_needs_lodging.id;


--
-- Name: kawacon2017_signupextra_shifts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_signupextra_shifts (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    shift_id integer NOT NULL
);


--
-- Name: kawacon2017_signupextra_shifts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_signupextra_shifts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_signupextra_shifts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_signupextra_shifts_id_seq OWNED BY public.kawacon2017_signupextra_shifts.id;


--
-- Name: kawacon2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kawacon2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_signupextra_special_diet_id_seq OWNED BY public.kawacon2017_signupextra_special_diet.id;


--
-- Name: kawacon2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kawacon2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kawacon2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kawacon2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kawacon2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kawacon2017_specialdiet_id_seq OWNED BY public.kawacon2017_specialdiet.id;


--
-- Name: kuplii2015_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2015_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: kuplii2015_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2015_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kuplii2015_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2015_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2015_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2015_signupextra_special_diet_id_seq OWNED BY public.kuplii2015_signupextra_special_diet.id;


--
-- Name: kuplii2015_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2015_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kuplii2015_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2015_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2015_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2015_specialdiet_id_seq OWNED BY public.kuplii2015_specialdiet.id;


--
-- Name: kuplii2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: kuplii2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kuplii2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2016_signupextra_special_diet_id_seq OWNED BY public.kuplii2016_signupextra_special_diet.id;


--
-- Name: kuplii2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kuplii2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2016_specialdiet_id_seq OWNED BY public.kuplii2016_specialdiet.id;


--
-- Name: kuplii2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: kuplii2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2017_signupextra_id_seq OWNED BY public.kuplii2017_signupextra.id;


--
-- Name: kuplii2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kuplii2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2017_signupextra_special_diet_id_seq OWNED BY public.kuplii2017_signupextra_special_diet.id;


--
-- Name: kuplii2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kuplii2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2017_specialdiet_id_seq OWNED BY public.kuplii2017_specialdiet.id;


--
-- Name: kuplii2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: kuplii2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2018_signupextra_id_seq OWNED BY public.kuplii2018_signupextra.id;


--
-- Name: kuplii2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: kuplii2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2018_signupextra_special_diet_id_seq OWNED BY public.kuplii2018_signupextra_special_diet.id;


--
-- Name: kuplii2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.kuplii2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: kuplii2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.kuplii2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: kuplii2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.kuplii2018_specialdiet_id_seq OWNED BY public.kuplii2018_specialdiet.id;


--
-- Name: labour_alternativesignupform; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_alternativesignupform (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(63) NOT NULL,
    signup_form_class_path character varying(63) NOT NULL,
    signup_extra_form_class_path character varying(63) NOT NULL,
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    signup_message text,
    event_id integer NOT NULL
);


--
-- Name: labour_alternativesignupform_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_alternativesignupform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_alternativesignupform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_alternativesignupform_id_seq OWNED BY public.labour_alternativesignupform.id;


--
-- Name: labour_common_qualifications_jvkortti; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_common_qualifications_jvkortti (
    personqualification_id integer NOT NULL,
    card_number character varying(13) NOT NULL,
    expiration_date date NOT NULL
);


--
-- Name: labour_emptysignupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_emptysignupextra (
    id integer NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: labour_emptysignupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_emptysignupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_emptysignupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_emptysignupextra_id_seq OWNED BY public.labour_emptysignupextra.id;


--
-- Name: labour_infolink; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_infolink (
    id integer NOT NULL,
    url character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    event_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: labour_infolink_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_infolink_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_infolink_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_infolink_id_seq OWNED BY public.labour_infolink.id;


--
-- Name: labour_job; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_job (
    id integer NOT NULL,
    title character varying(63) NOT NULL,
    job_category_id integer NOT NULL,
    slug character varying(255) NOT NULL
);


--
-- Name: labour_job_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_job_id_seq OWNED BY public.labour_job.id;


--
-- Name: labour_jobcategory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_jobcategory (
    id integer NOT NULL,
    name character varying(63) NOT NULL,
    slug character varying(255) NOT NULL,
    description text NOT NULL,
    public boolean NOT NULL,
    event_id integer NOT NULL,
    app_label character varying(63) NOT NULL
);


--
-- Name: labour_jobcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_jobcategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_jobcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_jobcategory_id_seq OWNED BY public.labour_jobcategory.id;


--
-- Name: labour_jobcategory_personnel_classes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_jobcategory_personnel_classes (
    id integer NOT NULL,
    jobcategory_id integer NOT NULL,
    personnelclass_id integer NOT NULL
);


--
-- Name: labour_jobcategory_personnel_classes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_jobcategory_personnel_classes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_jobcategory_personnel_classes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_jobcategory_personnel_classes_id_seq OWNED BY public.labour_jobcategory_personnel_classes.id;


--
-- Name: labour_jobcategory_required_qualifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_jobcategory_required_qualifications (
    id integer NOT NULL,
    jobcategory_id integer NOT NULL,
    qualification_id integer NOT NULL
);


--
-- Name: labour_jobcategory_required_qualifications_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_jobcategory_required_qualifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_jobcategory_required_qualifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_jobcategory_required_qualifications_id_seq OWNED BY public.labour_jobcategory_required_qualifications.id;


--
-- Name: labour_jobrequirement; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_jobrequirement (
    id integer NOT NULL,
    count integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    job_id integer NOT NULL
);


--
-- Name: labour_jobrequirement_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_jobrequirement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_jobrequirement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_jobrequirement_id_seq OWNED BY public.labour_jobrequirement.id;


--
-- Name: labour_laboureventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_laboureventmeta (
    event_id integer NOT NULL,
    registration_opens timestamp with time zone,
    registration_closes timestamp with time zone,
    work_begins timestamp with time zone NOT NULL,
    work_ends timestamp with time zone NOT NULL,
    monitor_email character varying(255) NOT NULL,
    contact_email character varying(255) NOT NULL,
    signup_message text,
    admin_group_id integer NOT NULL,
    signup_extra_content_type_id integer NOT NULL,
    work_certificate_signer text
);


--
-- Name: labour_obsoleteemptysignupextrav1; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_obsoleteemptysignupextrav1 (
    signup_id integer NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: labour_perk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_perk (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    name character varying(63) NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: labour_perk_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_perk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_perk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_perk_id_seq OWNED BY public.labour_perk.id;


--
-- Name: labour_personnelclass; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_personnelclass (
    id integer NOT NULL,
    app_label character varying(63) NOT NULL,
    name character varying(63) NOT NULL,
    slug character varying(255) NOT NULL,
    priority integer NOT NULL,
    event_id integer NOT NULL,
    icon_css_class character varying(63) NOT NULL
);


--
-- Name: labour_personnelclass_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_personnelclass_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_personnelclass_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_personnelclass_id_seq OWNED BY public.labour_personnelclass.id;


--
-- Name: labour_personnelclass_perks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_personnelclass_perks (
    id integer NOT NULL,
    personnelclass_id integer NOT NULL,
    perk_id integer NOT NULL
);


--
-- Name: labour_personnelclass_perks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_personnelclass_perks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_personnelclass_perks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_personnelclass_perks_id_seq OWNED BY public.labour_personnelclass_perks.id;


--
-- Name: labour_personqualification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_personqualification (
    id integer NOT NULL,
    person_id integer NOT NULL,
    qualification_id integer NOT NULL
);


--
-- Name: labour_personqualification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_personqualification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_personqualification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_personqualification_id_seq OWNED BY public.labour_personqualification.id;


--
-- Name: labour_qualification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_qualification (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    name character varying(63) NOT NULL,
    description text NOT NULL,
    qualification_extra_content_type_id integer
);


--
-- Name: labour_qualification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_qualification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_qualification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_qualification_id_seq OWNED BY public.labour_qualification.id;


--
-- Name: labour_shift; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_shift (
    id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    hours integer NOT NULL,
    notes text NOT NULL,
    job_id integer NOT NULL,
    signup_id integer NOT NULL,
    CONSTRAINT labour_shift_hours_check CHECK ((hours >= 0))
);


--
-- Name: labour_shift_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_shift_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_shift_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_shift_id_seq OWNED BY public.labour_shift.id;


--
-- Name: labour_signup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_signup (
    id integer NOT NULL,
    notes text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    xxx_interim_shifts text,
    job_title character varying(63) NOT NULL,
    is_active boolean NOT NULL,
    time_accepted timestamp with time zone,
    time_finished timestamp with time zone,
    time_complained timestamp with time zone,
    time_cancelled timestamp with time zone,
    time_rejected timestamp with time zone,
    time_arrived timestamp with time zone,
    time_work_accepted timestamp with time zone,
    time_reprimanded timestamp with time zone,
    alternative_signup_form_used_id integer,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    time_confirmation_requested timestamp with time zone
);


--
-- Name: labour_signup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_signup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_signup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_signup_id_seq OWNED BY public.labour_signup.id;


--
-- Name: labour_signup_job_categories; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_signup_job_categories (
    id integer NOT NULL,
    signup_id integer NOT NULL,
    jobcategory_id integer NOT NULL
);


--
-- Name: labour_signup_job_categories_accepted; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_signup_job_categories_accepted (
    id integer NOT NULL,
    signup_id integer NOT NULL,
    jobcategory_id integer NOT NULL
);


--
-- Name: labour_signup_job_categories_accepted_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_signup_job_categories_accepted_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_signup_job_categories_accepted_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_signup_job_categories_accepted_id_seq OWNED BY public.labour_signup_job_categories_accepted.id;


--
-- Name: labour_signup_job_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_signup_job_categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_signup_job_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_signup_job_categories_id_seq OWNED BY public.labour_signup_job_categories.id;


--
-- Name: labour_signup_job_categories_rejected; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_signup_job_categories_rejected (
    id integer NOT NULL,
    signup_id integer NOT NULL,
    jobcategory_id integer NOT NULL
);


--
-- Name: labour_signup_job_categories_rejected_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_signup_job_categories_rejected_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_signup_job_categories_rejected_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_signup_job_categories_rejected_id_seq OWNED BY public.labour_signup_job_categories_rejected.id;


--
-- Name: labour_signup_personnel_classes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_signup_personnel_classes (
    id integer NOT NULL,
    signup_id integer NOT NULL,
    personnelclass_id integer NOT NULL
);


--
-- Name: labour_signup_personnel_classes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_signup_personnel_classes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_signup_personnel_classes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_signup_personnel_classes_id_seq OWNED BY public.labour_signup_personnel_classes.id;


--
-- Name: labour_survey; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_survey (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    form_class_path character varying(255) NOT NULL,
    event_id integer NOT NULL,
    override_does_not_apply_message text NOT NULL
);


--
-- Name: labour_survey_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_survey_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_survey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_survey_id_seq OWNED BY public.labour_survey.id;


--
-- Name: labour_surveyrecord; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_surveyrecord (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    person_id integer NOT NULL,
    survey_id integer NOT NULL
);


--
-- Name: labour_surveyrecord_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_surveyrecord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_surveyrecord_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_surveyrecord_id_seq OWNED BY public.labour_surveyrecord.id;


--
-- Name: labour_workperiod; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.labour_workperiod (
    id integer NOT NULL,
    description character varying(63) NOT NULL,
    start_time timestamp with time zone,
    end_time timestamp with time zone,
    event_id integer NOT NULL
);


--
-- Name: labour_workperiod_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.labour_workperiod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: labour_workperiod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.labour_workperiod_id_seq OWNED BY public.labour_workperiod.id;


--
-- Name: lakeuscon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lakeuscon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: lakeuscon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lakeuscon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: lakeuscon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lakeuscon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lakeuscon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lakeuscon2016_signupextra_special_diet_id_seq OWNED BY public.lakeuscon2016_signupextra_special_diet.id;


--
-- Name: lakeuscon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lakeuscon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: lakeuscon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lakeuscon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lakeuscon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lakeuscon2016_specialdiet_id_seq OWNED BY public.lakeuscon2016_specialdiet.id;


--
-- Name: lippukala_code; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lippukala_code (
    id integer NOT NULL,
    created_on timestamp with time zone NOT NULL,
    status integer NOT NULL,
    used_on timestamp with time zone,
    used_at character varying(64) NOT NULL,
    prefix character varying(16) NOT NULL,
    code character varying(64) NOT NULL,
    literate_code character varying(256) NOT NULL,
    product_text character varying(512) NOT NULL,
    order_id integer NOT NULL
);


--
-- Name: lippukala_code_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lippukala_code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lippukala_code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lippukala_code_id_seq OWNED BY public.lippukala_code.id;


--
-- Name: lippukala_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lippukala_order (
    id integer NOT NULL,
    event character varying(32) NOT NULL,
    created_on timestamp with time zone NOT NULL,
    modified_on timestamp with time zone NOT NULL,
    reference_number character varying(64),
    address_text text NOT NULL,
    free_text text NOT NULL,
    comment text NOT NULL
);


--
-- Name: lippukala_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lippukala_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lippukala_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lippukala_order_id_seq OWNED BY public.lippukala_order.id;


--
-- Name: listings_externalevent; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listings_externalevent (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    name character varying(63) NOT NULL,
    description text NOT NULL,
    homepage_url character varying(255) NOT NULL,
    venue_name character varying(63) NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    public boolean NOT NULL,
    logo_file character varying(100) NOT NULL
);


--
-- Name: listings_externalevent_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.listings_externalevent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: listings_externalevent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.listings_externalevent_id_seq OWNED BY public.listings_externalevent.id;


--
-- Name: listings_listing; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listings_listing (
    id integer NOT NULL,
    hostname character varying(63) NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL
);


--
-- Name: listings_listing_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listings_listing_events (
    id integer NOT NULL,
    listing_id integer NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: listings_listing_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.listings_listing_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: listings_listing_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.listings_listing_events_id_seq OWNED BY public.listings_listing_events.id;


--
-- Name: listings_listing_external_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.listings_listing_external_events (
    id integer NOT NULL,
    listing_id integer NOT NULL,
    externalevent_id integer NOT NULL
);


--
-- Name: listings_listing_external_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.listings_listing_external_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: listings_listing_external_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.listings_listing_external_events_id_seq OWNED BY public.listings_listing_external_events.id;


--
-- Name: listings_listing_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.listings_listing_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: listings_listing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.listings_listing_id_seq OWNED BY public.listings_listing.id;


--
-- Name: mailings_message; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mailings_message (
    id integer NOT NULL,
    subject_template character varying(255) NOT NULL,
    body_template text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    sent_at timestamp with time zone,
    expired_at timestamp with time zone,
    recipient_id integer NOT NULL,
    channel character varying(5) NOT NULL
);


--
-- Name: mailings_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mailings_message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mailings_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mailings_message_id_seq OWNED BY public.mailings_message.id;


--
-- Name: mailings_personmessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mailings_personmessage (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    body_id integer NOT NULL,
    message_id integer NOT NULL,
    person_id integer NOT NULL,
    subject_id integer NOT NULL
);


--
-- Name: mailings_personmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mailings_personmessage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mailings_personmessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mailings_personmessage_id_seq OWNED BY public.mailings_personmessage.id;


--
-- Name: mailings_personmessagebody; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mailings_personmessagebody (
    id integer NOT NULL,
    digest character varying(63) NOT NULL,
    text text NOT NULL
);


--
-- Name: mailings_personmessagebody_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mailings_personmessagebody_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mailings_personmessagebody_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mailings_personmessagebody_id_seq OWNED BY public.mailings_personmessagebody.id;


--
-- Name: mailings_personmessagesubject; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mailings_personmessagesubject (
    id integer NOT NULL,
    digest character varying(63) NOT NULL,
    text character varying(255) NOT NULL
);


--
-- Name: mailings_personmessagesubject_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mailings_personmessagesubject_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mailings_personmessagesubject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mailings_personmessagesubject_id_seq OWNED BY public.mailings_personmessagesubject.id;


--
-- Name: mailings_recipientgroup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mailings_recipientgroup (
    id integer NOT NULL,
    app_label character varying(63) NOT NULL,
    verbose_name character varying(63) NOT NULL,
    event_id integer NOT NULL,
    group_id integer NOT NULL,
    job_category_id integer,
    personnel_class_id integer
);


--
-- Name: mailings_recipientgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mailings_recipientgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mailings_recipientgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mailings_recipientgroup_id_seq OWNED BY public.mailings_recipientgroup.id;


--
-- Name: matsucon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matsucon2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    more_info text NOT NULL,
    need_lodging boolean NOT NULL,
    night_work boolean NOT NULL,
    shirt_size character varying(8) NOT NULL,
    shift_type character varying(2) NOT NULL
);


--
-- Name: matsucon2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.matsucon2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: matsucon2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.matsucon2018_signupextra_id_seq OWNED BY public.matsucon2018_signupextra.id;


--
-- Name: matsucon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.matsucon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: matsucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.matsucon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: matsucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.matsucon2018_signupextra_special_diet_id_seq OWNED BY public.matsucon2018_signupextra_special_diet.id;


--
-- Name: membership_membership; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.membership_membership (
    id integer NOT NULL,
    organization_id integer NOT NULL,
    person_id integer NOT NULL,
    state character varying(10) NOT NULL,
    message text NOT NULL
);


--
-- Name: membership_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.membership_membership_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: membership_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.membership_membership_id_seq OWNED BY public.membership_membership.id;


--
-- Name: membership_membershipfeepayment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.membership_membershipfeepayment (
    id integer NOT NULL,
    payment_date date NOT NULL,
    member_id integer NOT NULL,
    term_id integer NOT NULL
);


--
-- Name: membership_membershipfeepayment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.membership_membershipfeepayment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: membership_membershipfeepayment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.membership_membershipfeepayment_id_seq OWNED BY public.membership_membershipfeepayment.id;


--
-- Name: membership_membershiporganizationmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.membership_membershiporganizationmeta (
    organization_id integer NOT NULL,
    admin_group_id integer NOT NULL,
    receiving_applications boolean NOT NULL,
    membership_requirements text NOT NULL,
    members_group_id integer NOT NULL
);


--
-- Name: membership_term; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.membership_term (
    id integer NOT NULL,
    title character varying(63) NOT NULL,
    start_date date NOT NULL,
    end_date date NOT NULL,
    entrance_fee_cents integer,
    membership_fee_cents integer,
    organization_id integer NOT NULL,
    payment_type character varying(13) NOT NULL,
    CONSTRAINT membership_term_entrance_fee_cents_check CHECK ((entrance_fee_cents >= 0)),
    CONSTRAINT membership_term_membership_fee_cents_check CHECK ((membership_fee_cents >= 0))
);


--
-- Name: membership_term_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.membership_term_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: membership_term_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.membership_term_id_seq OWNED BY public.membership_term.id;


--
-- Name: mimicon2016_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2016_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: mimicon2016_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2016_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2016_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2016_night_id_seq OWNED BY public.mimicon2016_night.id;


--
-- Name: mimicon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    construction boolean NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: mimicon2016_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2016_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: mimicon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2016_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2016_signupextra_lodging_needs_id_seq OWNED BY public.mimicon2016_signupextra_lodging_needs.id;


--
-- Name: mimicon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: mimicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2016_signupextra_special_diet_id_seq OWNED BY public.mimicon2016_signupextra_special_diet.id;


--
-- Name: mimicon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: mimicon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2016_specialdiet_id_seq OWNED BY public.mimicon2016_specialdiet.id;


--
-- Name: mimicon2018_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2018_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: mimicon2018_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2018_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2018_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2018_night_id_seq OWNED BY public.mimicon2018_night.id;


--
-- Name: mimicon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2018_signupextra (
    signup_id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    construction boolean NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL
);


--
-- Name: mimicon2018_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2018_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: mimicon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2018_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2018_signupextra_lodging_needs_id_seq OWNED BY public.mimicon2018_signupextra_lodging_needs.id;


--
-- Name: mimicon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: mimicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2018_signupextra_special_diet_id_seq OWNED BY public.mimicon2018_signupextra_special_diet.id;


--
-- Name: mimicon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.mimicon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: mimicon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.mimicon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: mimicon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.mimicon2018_specialdiet_id_seq OWNED BY public.mimicon2018_specialdiet.id;


--
-- Name: nexmo_deliverystatusfragment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nexmo_deliverystatusfragment (
    id integer NOT NULL,
    nexmo_message_id character varying(255) NOT NULL,
    error_code integer,
    status_msg character varying(50),
    status_timestamp timestamp with time zone,
    message_id integer NOT NULL
);


--
-- Name: nexmo_deliverystatusfragment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nexmo_deliverystatusfragment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nexmo_deliverystatusfragment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nexmo_deliverystatusfragment_id_seq OWNED BY public.nexmo_deliverystatusfragment.id;


--
-- Name: nexmo_inboundmessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nexmo_inboundmessage (
    id integer NOT NULL,
    nexmo_message_id character varying(255) NOT NULL,
    sender character varying(255) NOT NULL,
    nexmo_timestamp timestamp with time zone,
    receive_timestamp timestamp with time zone,
    message text NOT NULL
);


--
-- Name: nexmo_inboundmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nexmo_inboundmessage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nexmo_inboundmessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nexmo_inboundmessage_id_seq OWNED BY public.nexmo_inboundmessage.id;


--
-- Name: nexmo_inboundmessagefragment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nexmo_inboundmessagefragment (
    id integer NOT NULL,
    nexmo_message_id character varying(255) NOT NULL,
    sender character varying(255) NOT NULL,
    nexmo_timestamp timestamp with time zone,
    receive_timestamp timestamp with time zone NOT NULL,
    message text NOT NULL,
    concat_ref character varying(255),
    concat_part integer,
    concat_total integer
);


--
-- Name: nexmo_inboundmessagefragment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nexmo_inboundmessagefragment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nexmo_inboundmessagefragment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nexmo_inboundmessagefragment_id_seq OWNED BY public.nexmo_inboundmessagefragment.id;


--
-- Name: nexmo_outboundmessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nexmo_outboundmessage (
    id integer NOT NULL,
    message text NOT NULL,
    "to" character varying(50) NOT NULL,
    send_timestamp timestamp with time zone,
    send_status integer,
    status integer NOT NULL,
    sent_pieces integer,
    external_reference character varying(255) NOT NULL
);


--
-- Name: nexmo_outboundmessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nexmo_outboundmessage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nexmo_outboundmessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nexmo_outboundmessage_id_seq OWNED BY public.nexmo_outboundmessage.id;


--
-- Name: nippori2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nippori2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: nippori2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.nippori2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: nippori2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.nippori2017_signupextra_id_seq OWNED BY public.nippori2017_signupextra.id;


--
-- Name: oauth2_provider_accesstoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.oauth2_provider_accesstoken (
    id integer NOT NULL,
    token character varying(255) NOT NULL,
    expires timestamp with time zone NOT NULL,
    scope text NOT NULL,
    application_id integer NOT NULL,
    user_id integer
);


--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.oauth2_provider_accesstoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.oauth2_provider_accesstoken_id_seq OWNED BY public.oauth2_provider_accesstoken.id;


--
-- Name: oauth2_provider_application; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.oauth2_provider_application (
    id integer NOT NULL,
    client_id character varying(100) NOT NULL,
    redirect_uris text NOT NULL,
    client_type character varying(32) NOT NULL,
    authorization_grant_type character varying(32) NOT NULL,
    client_secret character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    user_id integer,
    skip_authorization boolean NOT NULL
);


--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.oauth2_provider_application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.oauth2_provider_application_id_seq OWNED BY public.oauth2_provider_application.id;


--
-- Name: oauth2_provider_grant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.oauth2_provider_grant (
    id integer NOT NULL,
    code character varying(255) NOT NULL,
    expires timestamp with time zone NOT NULL,
    redirect_uri character varying(255) NOT NULL,
    scope text NOT NULL,
    application_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.oauth2_provider_grant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.oauth2_provider_grant_id_seq OWNED BY public.oauth2_provider_grant.id;


--
-- Name: oauth2_provider_refreshtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.oauth2_provider_refreshtoken (
    id integer NOT NULL,
    token character varying(255) NOT NULL,
    access_token_id integer NOT NULL,
    application_id integer NOT NULL,
    user_id integer NOT NULL
);


--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.oauth2_provider_refreshtoken_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.oauth2_provider_refreshtoken_id_seq OWNED BY public.oauth2_provider_refreshtoken.id;


--
-- Name: payments_payment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payments_payment (
    id integer NOT NULL,
    test integer,
    "VERSION" character varying(4) NOT NULL,
    "STAMP" character varying(20) NOT NULL,
    "REFERENCE" character varying(20) NOT NULL,
    "PAYMENT" character varying(20) NOT NULL,
    "STATUS" integer NOT NULL,
    "ALGORITHM" integer NOT NULL,
    "MAC" character varying(32) NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: payments_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: payments_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments_payment.id;


--
-- Name: payments_paymentseventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payments_paymentseventmeta (
    event_id integer NOT NULL,
    checkout_password character varying(255) NOT NULL,
    checkout_merchant character varying(255) NOT NULL,
    checkout_delivery_date character varying(9) NOT NULL,
    admin_group_id integer NOT NULL
);


--
-- Name: popcult2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.popcult2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    y_u text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: popcult2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.popcult2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: popcult2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.popcult2017_signupextra_id_seq OWNED BY public.popcult2017_signupextra.id;


--
-- Name: popcult2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.popcult2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: popcult2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.popcult2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: popcult2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.popcult2017_signupextra_special_diet_id_seq OWNED BY public.popcult2017_signupextra_special_diet.id;


--
-- Name: popcultday2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.popcultday2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    y_u text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: popcultday2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.popcultday2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: popcultday2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.popcultday2018_signupextra_id_seq OWNED BY public.popcultday2018_signupextra.id;


--
-- Name: popcultday2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.popcultday2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: popcultday2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.popcultday2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: popcultday2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.popcultday2018_signupextra_special_diet_id_seq OWNED BY public.popcultday2018_signupextra_special_diet.id;


--
-- Name: programme_alternativeprogrammeform; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_alternativeprogrammeform (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(63) NOT NULL,
    description text,
    short_description text,
    programme_form_code character varying(63) NOT NULL,
    active_from timestamp with time zone,
    active_until timestamp with time zone,
    num_extra_invites integer NOT NULL,
    "order" integer NOT NULL,
    event_id integer NOT NULL,
    CONSTRAINT programme_alternativeprogrammeform_num_extra_invites_check CHECK ((num_extra_invites >= 0))
);


--
-- Name: programme_alternativeprogrammeform_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_alternativeprogrammeform_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_alternativeprogrammeform_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_alternativeprogrammeform_id_seq OWNED BY public.programme_alternativeprogrammeform.id;


--
-- Name: programme_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_category (
    id integer NOT NULL,
    title character varying(1023) NOT NULL,
    style character varying(15) NOT NULL,
    notes text NOT NULL,
    public boolean NOT NULL,
    event_id integer NOT NULL,
    slug character varying(255) NOT NULL
);


--
-- Name: programme_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_category_id_seq OWNED BY public.programme_category.id;


--
-- Name: programme_freeformorganizer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_freeformorganizer (
    id integer NOT NULL,
    text character varying(255) NOT NULL,
    programme_id integer NOT NULL
);


--
-- Name: programme_freeformorganizer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_freeformorganizer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_freeformorganizer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_freeformorganizer_id_seq OWNED BY public.programme_freeformorganizer.id;


--
-- Name: programme_invitation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_invitation (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    programme_id integer NOT NULL,
    role_id integer NOT NULL,
    code character varying(63) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    state character varying(8) NOT NULL,
    used_at timestamp with time zone,
    created_by_id integer,
    extra_invites integer NOT NULL,
    sire_id integer,
    CONSTRAINT programme_invitation_extra_invites_check CHECK ((extra_invites >= 0))
);


--
-- Name: programme_invitation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_invitation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_invitation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_invitation_id_seq OWNED BY public.programme_invitation.id;


--
-- Name: programme_programme; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programme (
    id integer NOT NULL,
    title character varying(1023) NOT NULL,
    description text NOT NULL,
    room_requirements text NOT NULL,
    tech_requirements text NOT NULL,
    requested_time_slot text NOT NULL,
    video_permission character varying(15) NOT NULL,
    notes_from_host text NOT NULL,
    start_time timestamp with time zone,
    length integer,
    notes text NOT NULL,
    category_id integer NOT NULL,
    room_id integer,
    state character varying(15) NOT NULL,
    end_time timestamp with time zone,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    slug character varying(255) NOT NULL,
    computer character varying(4) NOT NULL,
    encumbered_content character varying(7) NOT NULL,
    number_of_microphones integer NOT NULL,
    photography character varying(6) NOT NULL,
    use_audio character varying(7) NOT NULL,
    use_video character varying(7) NOT NULL,
    frozen boolean NOT NULL,
    video_link character varying(255) NOT NULL,
    rerun character varying(8) NOT NULL,
    approximate_length integer,
    is_age_restricted boolean NOT NULL,
    is_beginner_friendly boolean NOT NULL,
    is_children_friendly boolean NOT NULL,
    is_english_ok boolean NOT NULL,
    is_intended_for_experienced_participants boolean NOT NULL,
    max_players integer NOT NULL,
    min_players integer NOT NULL,
    other_author character varying(1023) NOT NULL,
    physical_play character varying(4) NOT NULL,
    rpg_system character varying(512) NOT NULL,
    three_word_description character varying(1023) NOT NULL,
    form_used_id integer,
    signup_link character varying(255) NOT NULL,
    length_from_host character varying(127),
    long_description text NOT NULL,
    ropecon2018_audience_size character varying(7),
    ropecon2018_characters integer,
    ropecon2018_genre_drama boolean NOT NULL,
    ropecon2018_genre_exploration boolean NOT NULL,
    ropecon2018_genre_fantasy boolean NOT NULL,
    ropecon2018_genre_historical boolean NOT NULL,
    ropecon2018_genre_horror boolean NOT NULL,
    ropecon2018_genre_humor boolean NOT NULL,
    ropecon2018_genre_modern boolean NOT NULL,
    ropecon2018_genre_mystery boolean NOT NULL,
    ropecon2018_genre_scifi boolean NOT NULL,
    ropecon2018_genre_war boolean NOT NULL,
    ropecon2018_is_no_language boolean NOT NULL,
    ropecon2018_is_panel_attendance_ok boolean NOT NULL,
    ropecon2018_prop_requirements character varying(200),
    ropecon2018_sessions integer,
    ropecon2018_signuplist character varying(15),
    ropecon2018_space_requirements text,
    ropecon2018_speciality character varying(100),
    ropecon2018_style_character_driven boolean NOT NULL,
    ropecon2018_style_combat_driven boolean NOT NULL,
    ropecon2018_style_light boolean NOT NULL,
    ropecon2018_style_rules_heavy boolean NOT NULL,
    ropecon2018_style_rules_light boolean NOT NULL,
    ropecon2018_style_serious boolean NOT NULL,
    ropecon2018_style_story_driven boolean NOT NULL,
    ropecon2018_kp_difficulty character varying(15),
    ropecon2018_kp_length character varying(2),
    ropecon2018_kp_tables character varying(5),
    language character varying(2) NOT NULL,
    CONSTRAINT programme_programme_max_players_check CHECK ((max_players >= 0)),
    CONSTRAINT programme_programme_min_players_check CHECK ((min_players >= 0)),
    CONSTRAINT programme_programme_ropecon2018_characters_check CHECK ((ropecon2018_characters >= 0)),
    CONSTRAINT programme_programme_ropecon2018_sessions_check CHECK ((ropecon2018_sessions >= 0))
);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programme_hitpoint2017_preferred_time_slots (
    id integer NOT NULL,
    programme_id integer NOT NULL,
    timeslot_id integer NOT NULL
);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programme_hitpoint2017_preferred_time_slots_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programme_hitpoint2017_preferred_time_slots_id_seq OWNED BY public.programme_programme_hitpoint2017_preferred_time_slots.id;


--
-- Name: programme_programme_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programme_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programme_id_seq OWNED BY public.programme_programme.id;


--
-- Name: programme_programme_ropecon2018_preferred_time_slots; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programme_ropecon2018_preferred_time_slots (
    id integer NOT NULL,
    programme_id integer NOT NULL,
    timeslot_id integer NOT NULL
);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programme_ropecon2018_preferred_time_slots_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programme_ropecon2018_preferred_time_slots_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programme_ropecon2018_preferred_time_slots_id_seq OWNED BY public.programme_programme_ropecon2018_preferred_time_slots.id;


--
-- Name: programme_programme_tags; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programme_tags (
    id integer NOT NULL,
    programme_id integer NOT NULL,
    tag_id integer NOT NULL
);


--
-- Name: programme_programme_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programme_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programme_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programme_tags_id_seq OWNED BY public.programme_programme_tags.id;


--
-- Name: programme_programmeeventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programmeeventmeta (
    event_id integer NOT NULL,
    contact_email character varying(255) NOT NULL,
    admin_group_id integer NOT NULL,
    public_from timestamp with time zone,
    accepting_cold_offers_from timestamp with time zone,
    accepting_cold_offers_until timestamp with time zone,
    schedule_layout character varying(10) NOT NULL
);


--
-- Name: programme_programmefeedback; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programmefeedback (
    id integer NOT NULL,
    author_ip_address character varying(48) NOT NULL,
    is_anonymous boolean NOT NULL,
    feedback text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    hidden_at timestamp with time zone,
    author_id integer,
    hidden_by_id integer,
    programme_id integer NOT NULL
);


--
-- Name: programme_programmefeedback_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programmefeedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programmefeedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programmefeedback_id_seq OWNED BY public.programme_programmefeedback.id;


--
-- Name: programme_programmerole; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_programmerole (
    id integer NOT NULL,
    person_id integer NOT NULL,
    programme_id integer NOT NULL,
    role_id integer NOT NULL,
    invitation_id integer,
    extra_invites integer NOT NULL,
    is_active boolean NOT NULL,
    CONSTRAINT programme_programmerole_extra_invites_check CHECK ((extra_invites >= 0))
);


--
-- Name: programme_programmerole_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_programmerole_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_programmerole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_programmerole_id_seq OWNED BY public.programme_programmerole.id;


--
-- Name: programme_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_role (
    id integer NOT NULL,
    title character varying(1023) NOT NULL,
    require_contact_info boolean NOT NULL,
    is_default boolean NOT NULL,
    is_public boolean NOT NULL,
    personnel_class_id integer NOT NULL,
    priority integer NOT NULL,
    override_public_title character varying(63) NOT NULL
);


--
-- Name: programme_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_role_id_seq OWNED BY public.programme_role.id;


--
-- Name: programme_room; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_room (
    id integer NOT NULL,
    name character varying(1023) NOT NULL,
    notes text NOT NULL,
    slug character varying(255) NOT NULL,
    event_id integer
);


--
-- Name: programme_room_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_room_id_seq OWNED BY public.programme_room.id;


--
-- Name: programme_specialstarttime; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_specialstarttime (
    id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: programme_specialstarttime_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_specialstarttime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_specialstarttime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_specialstarttime_id_seq OWNED BY public.programme_specialstarttime.id;


--
-- Name: programme_tag; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_tag (
    id integer NOT NULL,
    title character varying(63) NOT NULL,
    "order" integer NOT NULL,
    style character varying(15) NOT NULL,
    event_id integer NOT NULL,
    slug character varying(255) NOT NULL
);


--
-- Name: programme_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_tag_id_seq OWNED BY public.programme_tag.id;


--
-- Name: programme_timeblock; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_timeblock (
    id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: programme_timeblock_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_timeblock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_timeblock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_timeblock_id_seq OWNED BY public.programme_timeblock.id;


--
-- Name: programme_view; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_view (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    public boolean NOT NULL,
    "order" integer NOT NULL,
    event_id integer NOT NULL,
    end_time timestamp with time zone,
    start_time timestamp with time zone
);


--
-- Name: programme_view_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_view_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_view_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_view_id_seq OWNED BY public.programme_view.id;


--
-- Name: programme_viewroom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.programme_viewroom (
    id integer NOT NULL,
    "order" integer NOT NULL,
    room_id integer NOT NULL,
    view_id integer NOT NULL
);


--
-- Name: programme_viewroom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.programme_viewroom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: programme_viewroom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.programme_viewroom_id_seq OWNED BY public.programme_viewroom.id;


--
-- Name: ropecon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ropecon2018_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: ropecon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ropecon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: ropecon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ropecon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ropecon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ropecon2018_signupextra_special_diet_id_seq OWNED BY public.ropecon2018_signupextra_special_diet.id;


--
-- Name: ropecon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ropecon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: ropecon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ropecon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ropecon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ropecon2018_specialdiet_id_seq OWNED BY public.ropecon2018_specialdiet.id;


--
-- Name: ropecon2018_timeslot; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ropecon2018_timeslot (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: ropecon2018_timeslot_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ropecon2018_timeslot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ropecon2018_timeslot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ropecon2018_timeslot_id_seq OWNED BY public.ropecon2018_timeslot.id;


--
-- Name: shippocon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shippocon2016_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    special_diet_other text NOT NULL,
    total_work character varying(15) NOT NULL,
    shift_type character varying(15) NOT NULL,
    working_days character varying(4) NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: shippocon2016_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.shippocon2016_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shippocon2016_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.shippocon2016_signupextra_id_seq OWNED BY public.shippocon2016_signupextra.id;


--
-- Name: shippocon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shippocon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: shippocon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.shippocon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shippocon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.shippocon2016_signupextra_special_diet_id_seq OWNED BY public.shippocon2016_signupextra_special_diet.id;


--
-- Name: shippocon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shippocon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: shippocon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.shippocon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shippocon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.shippocon2016_specialdiet_id_seq OWNED BY public.shippocon2016_specialdiet.id;


--
-- Name: sms_hotword; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_hotword (
    id integer NOT NULL,
    hotword character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    valid_from timestamp with time zone NOT NULL,
    valid_to timestamp with time zone NOT NULL,
    assigned_event_id integer NOT NULL
);


--
-- Name: sms_hotword_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_hotword_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_hotword_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_hotword_id_seq OWNED BY public.sms_hotword.id;


--
-- Name: sms_nominee; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_nominee (
    id integer NOT NULL,
    number integer NOT NULL,
    name character varying(255)
);


--
-- Name: sms_nominee_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_nominee_category (
    id integer NOT NULL,
    nominee_id integer NOT NULL,
    votecategory_id integer NOT NULL
);


--
-- Name: sms_nominee_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_nominee_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_nominee_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_nominee_category_id_seq OWNED BY public.sms_nominee_category.id;


--
-- Name: sms_nominee_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_nominee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_nominee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_nominee_id_seq OWNED BY public.sms_nominee.id;


--
-- Name: sms_smseventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_smseventmeta (
    event_id integer NOT NULL,
    sms_enabled boolean NOT NULL,
    current boolean NOT NULL,
    used_credit integer NOT NULL,
    admin_group_id integer NOT NULL
);


--
-- Name: sms_smsmessagein; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_smsmessagein (
    id integer NOT NULL,
    message_id integer NOT NULL,
    "SMSEventMeta_id" integer NOT NULL
);


--
-- Name: sms_smsmessagein_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_smsmessagein_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_smsmessagein_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_smsmessagein_id_seq OWNED BY public.sms_smsmessagein.id;


--
-- Name: sms_smsmessageout; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_smsmessageout (
    id integer NOT NULL,
    message text NOT NULL,
    "to" character varying(20) NOT NULL,
    event_id integer NOT NULL,
    ref_id integer
);


--
-- Name: sms_smsmessageout_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_smsmessageout_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_smsmessageout_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_smsmessageout_id_seq OWNED BY public.sms_smsmessageout.id;


--
-- Name: sms_vote; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_vote (
    id integer NOT NULL,
    vote_id integer NOT NULL,
    category_id integer NOT NULL,
    message_id integer NOT NULL
);


--
-- Name: sms_vote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_vote_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_vote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_vote_id_seq OWNED BY public.sms_vote.id;


--
-- Name: sms_votecategory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sms_votecategory (
    id integer NOT NULL,
    category character varying(255) NOT NULL,
    slug character varying(20) NOT NULL,
    "primary" boolean NOT NULL,
    hotword_id integer NOT NULL
);


--
-- Name: sms_votecategory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sms_votecategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sms_votecategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sms_votecategory_id_seq OWNED BY public.sms_votecategory.id;


--
-- Name: surveys_eventsurvey; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.surveys_eventsurvey (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    model jsonb NOT NULL,
    slug character varying(255) NOT NULL,
    event_id integer NOT NULL,
    owner_id integer
);


--
-- Name: surveys_eventsurvey_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.surveys_eventsurvey_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: surveys_eventsurvey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.surveys_eventsurvey_id_seq OWNED BY public.surveys_eventsurvey.id;


--
-- Name: surveys_eventsurveyresult; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.surveys_eventsurveyresult (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    model jsonb NOT NULL,
    author_ip_address character varying(48) NOT NULL,
    author_id integer,
    survey_id integer NOT NULL
);


--
-- Name: surveys_eventsurveyresult_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.surveys_eventsurveyresult_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: surveys_eventsurveyresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.surveys_eventsurveyresult_id_seq OWNED BY public.surveys_eventsurveyresult.id;


--
-- Name: surveys_globalsurvey; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.surveys_globalsurvey (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    model jsonb NOT NULL,
    slug character varying(255) NOT NULL,
    owner_id integer
);


--
-- Name: surveys_globalsurvey_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.surveys_globalsurvey_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: surveys_globalsurvey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.surveys_globalsurvey_id_seq OWNED BY public.surveys_globalsurvey.id;


--
-- Name: surveys_globalsurveyresult; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.surveys_globalsurveyresult (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    model jsonb NOT NULL,
    author_ip_address character varying(48) NOT NULL,
    author_id integer,
    survey_id integer NOT NULL
);


--
-- Name: surveys_globalsurveyresult_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.surveys_globalsurveyresult_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: surveys_globalsurveyresult_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.surveys_globalsurveyresult_id_seq OWNED BY public.surveys_globalsurveyresult.id;


--
-- Name: tickets_accommodationinformation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_accommodationinformation (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    phone_number character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    order_product_id integer
);


--
-- Name: tickets_accommodationinformation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_accommodationinformation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_accommodationinformation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_accommodationinformation_id_seq OWNED BY public.tickets_accommodationinformation.id;


--
-- Name: tickets_accommodationinformation_limit_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_accommodationinformation_limit_groups (
    id integer NOT NULL,
    accommodationinformation_id integer NOT NULL,
    limitgroup_id integer NOT NULL
);


--
-- Name: tickets_accommodationinformation_limit_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_accommodationinformation_limit_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_accommodationinformation_limit_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_accommodationinformation_limit_groups_id_seq OWNED BY public.tickets_accommodationinformation_limit_groups.id;


--
-- Name: tickets_batch; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_batch (
    id integer NOT NULL,
    create_time timestamp with time zone NOT NULL,
    delivery_time timestamp with time zone,
    event_id integer NOT NULL
);


--
-- Name: tickets_batch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_batch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_batch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_batch_id_seq OWNED BY public.tickets_batch.id;


--
-- Name: tickets_customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_customer (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    address character varying(200) NOT NULL,
    zip_code character varying(5) NOT NULL,
    city character varying(255) NOT NULL,
    email character varying(254) NOT NULL,
    allow_marketing_email boolean NOT NULL,
    phone_number character varying(30)
);


--
-- Name: tickets_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_customer_id_seq OWNED BY public.tickets_customer.id;


--
-- Name: tickets_limitgroup; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_limitgroup (
    id integer NOT NULL,
    description character varying(255) NOT NULL,
    "limit" integer NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: tickets_limitgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_limitgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_limitgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_limitgroup_id_seq OWNED BY public.tickets_limitgroup.id;


--
-- Name: tickets_order; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_order (
    id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    confirm_time timestamp with time zone,
    ip_address character varying(15),
    payment_date date,
    cancellation_time timestamp with time zone,
    reference_number character varying(31) NOT NULL,
    batch_id integer,
    customer_id integer,
    event_id integer NOT NULL
);


--
-- Name: tickets_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_order_id_seq OWNED BY public.tickets_order.id;


--
-- Name: tickets_orderproduct; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_orderproduct (
    id integer NOT NULL,
    count integer NOT NULL,
    order_id integer NOT NULL,
    product_id integer NOT NULL
);


--
-- Name: tickets_orderproduct_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_orderproduct_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_orderproduct_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_orderproduct_id_seq OWNED BY public.tickets_orderproduct.id;


--
-- Name: tickets_product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_product (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    internal_description character varying(255),
    description text NOT NULL,
    mail_description text,
    price_cents integer NOT NULL,
    requires_shipping boolean NOT NULL,
    electronic_ticket boolean NOT NULL,
    available boolean NOT NULL,
    notify_email character varying(100),
    ordering integer NOT NULL,
    event_id integer NOT NULL,
    requires_accommodation_information boolean NOT NULL,
    requires_shirt_size boolean NOT NULL,
    electronic_tickets_per_product integer NOT NULL,
    override_electronic_ticket_title character varying(100) NOT NULL,
    CONSTRAINT tickets_product_electronic_tickets_per_product_check CHECK ((electronic_tickets_per_product >= 0))
);


--
-- Name: tickets_product_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_product_id_seq OWNED BY public.tickets_product.id;


--
-- Name: tickets_product_limit_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_product_limit_groups (
    id integer NOT NULL,
    product_id integer NOT NULL,
    limitgroup_id integer NOT NULL
);


--
-- Name: tickets_product_limit_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_product_limit_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_product_limit_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_product_limit_groups_id_seq OWNED BY public.tickets_product_limit_groups.id;


--
-- Name: tickets_shirtorder; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_shirtorder (
    id integer NOT NULL,
    count integer NOT NULL,
    order_id integer NOT NULL,
    size_id integer NOT NULL,
    CONSTRAINT tickets_shirtorder_count_check CHECK ((count >= 0))
);


--
-- Name: tickets_shirtorder_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_shirtorder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_shirtorder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_shirtorder_id_seq OWNED BY public.tickets_shirtorder.id;


--
-- Name: tickets_shirtsize; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_shirtsize (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    available boolean NOT NULL,
    type_id integer NOT NULL
);


--
-- Name: tickets_shirtsize_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_shirtsize_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_shirtsize_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_shirtsize_id_seq OWNED BY public.tickets_shirtsize.id;


--
-- Name: tickets_shirttype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_shirttype (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    available boolean NOT NULL,
    event_id integer NOT NULL
);


--
-- Name: tickets_shirttype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tickets_shirttype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tickets_shirttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tickets_shirttype_id_seq OWNED BY public.tickets_shirttype.id;


--
-- Name: tickets_ticketseventmeta; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tickets_ticketseventmeta (
    event_id integer NOT NULL,
    shipping_and_handling_cents integer NOT NULL,
    due_days integer NOT NULL,
    ticket_sales_starts timestamp with time zone,
    ticket_sales_ends timestamp with time zone,
    reference_number_template character varying(31) NOT NULL,
    contact_email character varying(255) NOT NULL,
    ticket_spam_email character varying(255) NOT NULL,
    reservation_seconds integer NOT NULL,
    ticket_free_text text NOT NULL,
    admin_group_id integer NOT NULL,
    front_page_text text NOT NULL,
    print_logo_height_mm integer NOT NULL,
    print_logo_path character varying(255) NOT NULL,
    print_logo_width_mm integer NOT NULL,
    receipt_footer character varying(1023) NOT NULL,
    pos_access_group_id integer
);


--
-- Name: tracon11_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon11_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_night_id_seq OWNED BY public.tracon11_night.id;


--
-- Name: tracon11_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    email_alias character varying(32) NOT NULL,
    is_active boolean NOT NULL,
    shift_wishes text NOT NULL
);


--
-- Name: tracon11_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: tracon11_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_signupextra_lodging_needs_id_seq OWNED BY public.tracon11_signupextra_lodging_needs.id;


--
-- Name: tracon11_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tracon11_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_signupextra_special_diet_id_seq OWNED BY public.tracon11_signupextra_special_diet.id;


--
-- Name: tracon11_signupextrav2; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextrav2 (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    shift_wishes text NOT NULL,
    email_alias character varying(32) NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    afterparty_participation boolean NOT NULL,
    outward_coach_departure_time character varying(5) NOT NULL,
    return_coach_departure_time character varying(5) NOT NULL,
    afterparty_coaches_changed boolean NOT NULL
);


--
-- Name: tracon11_signupextrav2_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_signupextrav2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_signupextrav2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_signupextrav2_id_seq OWNED BY public.tracon11_signupextrav2.id;


--
-- Name: tracon11_signupextrav2_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextrav2_lodging_needs (
    id integer NOT NULL,
    signupextrav2_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: tracon11_signupextrav2_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_signupextrav2_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_signupextrav2_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_signupextrav2_lodging_needs_id_seq OWNED BY public.tracon11_signupextrav2_lodging_needs.id;


--
-- Name: tracon11_signupextrav2_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_signupextrav2_special_diet (
    id integer NOT NULL,
    signupextrav2_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tracon11_signupextrav2_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_signupextrav2_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_signupextrav2_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_signupextrav2_special_diet_id_seq OWNED BY public.tracon11_signupextrav2_special_diet.id;


--
-- Name: tracon11_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon11_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon11_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon11_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon11_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon11_specialdiet_id_seq OWNED BY public.tracon11_specialdiet.id;


--
-- Name: tracon2017_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon2017_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_night_id_seq OWNED BY public.tracon2017_night.id;


--
-- Name: tracon2017_poison; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_poison (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon2017_poison_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_poison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_poison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_poison_id_seq OWNED BY public.tracon2017_poison.id;


--
-- Name: tracon2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    shift_wishes text NOT NULL,
    email_alias character varying(32) NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    afterparty_coaches_changed boolean NOT NULL,
    afterparty_participation boolean NOT NULL,
    outward_coach_departure_time character varying(5) NOT NULL,
    return_coach_departure_time character varying(5) NOT NULL
);


--
-- Name: tracon2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_signupextra_id_seq OWNED BY public.tracon2017_signupextra.id;


--
-- Name: tracon2017_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: tracon2017_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_signupextra_lodging_needs_id_seq OWNED BY public.tracon2017_signupextra_lodging_needs.id;


--
-- Name: tracon2017_signupextra_pick_your_poison; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_signupextra_pick_your_poison (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    poison_id integer NOT NULL
);


--
-- Name: tracon2017_signupextra_pick_your_poison_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_signupextra_pick_your_poison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_signupextra_pick_your_poison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_signupextra_pick_your_poison_id_seq OWNED BY public.tracon2017_signupextra_pick_your_poison.id;


--
-- Name: tracon2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tracon2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2017_signupextra_special_diet_id_seq OWNED BY public.tracon2017_signupextra_special_diet.id;


--
-- Name: tracon2018_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon2018_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_night_id_seq OWNED BY public.tracon2018_night.id;


--
-- Name: tracon2018_poison; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_poison (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon2018_poison_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_poison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_poison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_poison_id_seq OWNED BY public.tracon2018_poison.id;


--
-- Name: tracon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    shift_wishes text NOT NULL,
    email_alias character varying(32) NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    afterparty_coaches_changed boolean NOT NULL,
    afterparty_participation boolean NOT NULL,
    outward_coach_departure_time character varying(5) NOT NULL,
    return_coach_departure_time character varying(5) NOT NULL,
    willing_to_bartend boolean NOT NULL
);


--
-- Name: tracon2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_signupextra_id_seq OWNED BY public.tracon2018_signupextra.id;


--
-- Name: tracon2018_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: tracon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_signupextra_lodging_needs_id_seq OWNED BY public.tracon2018_signupextra_lodging_needs.id;


--
-- Name: tracon2018_signupextra_pick_your_poison; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_signupextra_pick_your_poison (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    poison_id integer NOT NULL
);


--
-- Name: tracon2018_signupextra_pick_your_poison_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_signupextra_pick_your_poison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_signupextra_pick_your_poison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_signupextra_pick_your_poison_id_seq OWNED BY public.tracon2018_signupextra_pick_your_poison.id;


--
-- Name: tracon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tracon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon2018_signupextra_special_diet_id_seq OWNED BY public.tracon2018_signupextra_special_diet.id;


--
-- Name: tracon9_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon9_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon9_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon9_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon9_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon9_night_id_seq OWNED BY public.tracon9_night.id;


--
-- Name: tracon9_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon9_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    construction boolean NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: tracon9_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon9_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: tracon9_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon9_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon9_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon9_signupextra_lodging_needs_id_seq OWNED BY public.tracon9_signupextra_lodging_needs.id;


--
-- Name: tracon9_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon9_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tracon9_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon9_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon9_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon9_signupextra_special_diet_id_seq OWNED BY public.tracon9_signupextra_special_diet.id;


--
-- Name: tracon9_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracon9_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tracon9_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracon9_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracon9_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracon9_specialdiet_id_seq OWNED BY public.tracon9_specialdiet.id;


--
-- Name: traconx_night; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traconx_night (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: traconx_night_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traconx_night_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traconx_night_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traconx_night_id_seq OWNED BY public.traconx_night.id;


--
-- Name: traconx_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traconx_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    overseer boolean NOT NULL,
    want_certificate boolean NOT NULL,
    certificate_delivery_address text NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    email_alias character varying(32) NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: traconx_signupextra_lodging_needs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traconx_signupextra_lodging_needs (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    night_id integer NOT NULL
);


--
-- Name: traconx_signupextra_lodging_needs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traconx_signupextra_lodging_needs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traconx_signupextra_lodging_needs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traconx_signupextra_lodging_needs_id_seq OWNED BY public.traconx_signupextra_lodging_needs.id;


--
-- Name: traconx_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traconx_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: traconx_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traconx_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traconx_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traconx_signupextra_special_diet_id_seq OWNED BY public.traconx_signupextra_special_diet.id;


--
-- Name: traconx_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traconx_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: traconx_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traconx_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traconx_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traconx_specialdiet_id_seq OWNED BY public.traconx_specialdiet.id;


--
-- Name: tylycon2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tylycon2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    motivation text NOT NULL,
    shift_cleanup boolean NOT NULL,
    shift_setup boolean NOT NULL
);


--
-- Name: tylycon2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tylycon2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tylycon2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tylycon2017_signupextra_id_seq OWNED BY public.tylycon2017_signupextra.id;


--
-- Name: tylycon2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tylycon2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: tylycon2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tylycon2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tylycon2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tylycon2017_signupextra_special_diet_id_seq OWNED BY public.tylycon2017_signupextra_special_diet.id;


--
-- Name: tylycon2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tylycon2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: tylycon2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tylycon2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tylycon2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tylycon2017_specialdiet_id_seq OWNED BY public.tylycon2017_specialdiet.id;


--
-- Name: worldcon75_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.worldcon75_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    special_diet_other text NOT NULL,
    shift_wishes text NOT NULL,
    prior_experience text NOT NULL,
    free_text text NOT NULL,
    is_attending_member boolean NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: worldcon75_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.worldcon75_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: worldcon75_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.worldcon75_signupextra_id_seq OWNED BY public.worldcon75_signupextra.id;


--
-- Name: worldcon75_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.worldcon75_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: worldcon75_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.worldcon75_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: worldcon75_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.worldcon75_signupextra_special_diet_id_seq OWNED BY public.worldcon75_signupextra_special_diet.id;


--
-- Name: yukicon2016_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2016_signupextra (
    signup_id integer NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    construction boolean NOT NULL,
    want_certificate boolean NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    is_active boolean NOT NULL
);


--
-- Name: yukicon2016_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2016_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: yukicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2016_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2016_signupextra_special_diet_id_seq OWNED BY public.yukicon2016_signupextra_special_diet.id;


--
-- Name: yukicon2016_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2016_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2016_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2016_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2016_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2016_specialdiet_id_seq OWNED BY public.yukicon2016_specialdiet.id;


--
-- Name: yukicon2017_eventday; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2017_eventday (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2017_eventday_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2017_eventday_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2017_eventday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2017_eventday_id_seq OWNED BY public.yukicon2017_eventday.id;


--
-- Name: yukicon2017_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2017_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: yukicon2017_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2017_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2017_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2017_signupextra_id_seq OWNED BY public.yukicon2017_signupextra.id;


--
-- Name: yukicon2017_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2017_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: yukicon2017_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2017_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2017_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2017_signupextra_special_diet_id_seq OWNED BY public.yukicon2017_signupextra_special_diet.id;


--
-- Name: yukicon2017_signupextra_work_days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2017_signupextra_work_days (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    eventday_id integer NOT NULL
);


--
-- Name: yukicon2017_signupextra_work_days_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2017_signupextra_work_days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2017_signupextra_work_days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2017_signupextra_work_days_id_seq OWNED BY public.yukicon2017_signupextra_work_days.id;


--
-- Name: yukicon2017_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2017_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2017_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2017_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2017_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2017_specialdiet_id_seq OWNED BY public.yukicon2017_specialdiet.id;


--
-- Name: yukicon2018_eventday; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2018_eventday (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2018_eventday_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2018_eventday_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2018_eventday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2018_eventday_id_seq OWNED BY public.yukicon2018_eventday.id;


--
-- Name: yukicon2018_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2018_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL,
    shirt_size character varying(8) NOT NULL
);


--
-- Name: yukicon2018_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2018_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2018_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2018_signupextra_id_seq OWNED BY public.yukicon2018_signupextra.id;


--
-- Name: yukicon2018_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2018_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: yukicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2018_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2018_signupextra_special_diet_id_seq OWNED BY public.yukicon2018_signupextra_special_diet.id;


--
-- Name: yukicon2018_signupextra_work_days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2018_signupextra_work_days (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    eventday_id integer NOT NULL
);


--
-- Name: yukicon2018_signupextra_work_days_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2018_signupextra_work_days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2018_signupextra_work_days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2018_signupextra_work_days_id_seq OWNED BY public.yukicon2018_signupextra_work_days.id;


--
-- Name: yukicon2018_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2018_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2018_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2018_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2018_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2018_specialdiet_id_seq OWNED BY public.yukicon2018_specialdiet.id;


--
-- Name: yukicon2019_eventday; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2019_eventday (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2019_eventday_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2019_eventday_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2019_eventday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2019_eventday_id_seq OWNED BY public.yukicon2019_eventday.id;


--
-- Name: yukicon2019_signupextra; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2019_signupextra (
    id integer NOT NULL,
    is_active boolean NOT NULL,
    shift_type character varying(15) NOT NULL,
    total_work character varying(15) NOT NULL,
    want_certificate boolean NOT NULL,
    shirt_size character varying(8) NOT NULL,
    special_diet_other text NOT NULL,
    prior_experience text NOT NULL,
    shift_wishes text NOT NULL,
    free_text text NOT NULL,
    event_id integer NOT NULL,
    person_id integer NOT NULL
);


--
-- Name: yukicon2019_signupextra_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2019_signupextra_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2019_signupextra_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2019_signupextra_id_seq OWNED BY public.yukicon2019_signupextra.id;


--
-- Name: yukicon2019_signupextra_special_diet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2019_signupextra_special_diet (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    specialdiet_id integer NOT NULL
);


--
-- Name: yukicon2019_signupextra_special_diet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2019_signupextra_special_diet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2019_signupextra_special_diet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2019_signupextra_special_diet_id_seq OWNED BY public.yukicon2019_signupextra_special_diet.id;


--
-- Name: yukicon2019_signupextra_work_days; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2019_signupextra_work_days (
    id integer NOT NULL,
    signupextra_id integer NOT NULL,
    eventday_id integer NOT NULL
);


--
-- Name: yukicon2019_signupextra_work_days_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2019_signupextra_work_days_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2019_signupextra_work_days_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2019_signupextra_work_days_id_seq OWNED BY public.yukicon2019_signupextra_work_days.id;


--
-- Name: yukicon2019_specialdiet; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yukicon2019_specialdiet (
    id integer NOT NULL,
    name character varying(63) NOT NULL
);


--
-- Name: yukicon2019_specialdiet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yukicon2019_specialdiet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yukicon2019_specialdiet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yukicon2019_specialdiet_id_seq OWNED BY public.yukicon2019_specialdiet.id;


--
-- Name: access_emailalias id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias ALTER COLUMN id SET DEFAULT nextval('public.access_emailalias_id_seq'::regclass);


--
-- Name: access_emailaliasdomain id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliasdomain ALTER COLUMN id SET DEFAULT nextval('public.access_emailaliasdomain_id_seq'::regclass);


--
-- Name: access_emailaliastype id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliastype ALTER COLUMN id SET DEFAULT nextval('public.access_emailaliastype_id_seq'::regclass);


--
-- Name: access_grantedprivilege id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_grantedprivilege ALTER COLUMN id SET DEFAULT nextval('public.access_grantedprivilege_id_seq'::regclass);


--
-- Name: access_groupemailaliasgrant id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupemailaliasgrant ALTER COLUMN id SET DEFAULT nextval('public.access_groupemailaliasgrant_id_seq'::regclass);


--
-- Name: access_groupprivilege id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege ALTER COLUMN id SET DEFAULT nextval('public.access_groupprivilege_id_seq'::regclass);


--
-- Name: access_internalemailalias id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_internalemailalias ALTER COLUMN id SET DEFAULT nextval('public.access_internalemailalias_id_seq'::regclass);


--
-- Name: access_privilege id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_privilege ALTER COLUMN id SET DEFAULT nextval('public.access_privilege_id_seq'::regclass);


--
-- Name: access_slackaccess id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_slackaccess ALTER COLUMN id SET DEFAULT nextval('public.access_slackaccess_id_seq'::regclass);


--
-- Name: access_smtppassword id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtppassword ALTER COLUMN id SET DEFAULT nextval('public.access_smtppassword_id_seq'::regclass);


--
-- Name: access_smtpserver id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver ALTER COLUMN id SET DEFAULT nextval('public.access_smtpserver_id_seq'::regclass);


--
-- Name: access_smtpserver_domains id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver_domains ALTER COLUMN id SET DEFAULT nextval('public.access_smtpserver_domains_id_seq'::regclass);


--
-- Name: aicon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.aicon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: aicon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.aicon2016_specialdiet_id_seq'::regclass);


--
-- Name: aicon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.aicon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: aicon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.aicon2018_specialdiet_id_seq'::regclass);


--
-- Name: animecon2015_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_night ALTER COLUMN id SET DEFAULT nextval('public.animecon2015_night_id_seq'::regclass);


--
-- Name: animecon2015_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.animecon2015_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: animecon2015_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.animecon2015_signupextra_special_diet_id_seq'::regclass);


--
-- Name: animecon2015_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.animecon2015_specialdiet_id_seq'::regclass);


--
-- Name: animecon2016_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_night ALTER COLUMN id SET DEFAULT nextval('public.animecon2016_night_id_seq'::regclass);


--
-- Name: animecon2016_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.animecon2016_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: animecon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.animecon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: animecon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.animecon2016_specialdiet_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: badges_badge id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge ALTER COLUMN id SET DEFAULT nextval('public.badges_badge_id_seq'::regclass);


--
-- Name: badges_batch id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_batch ALTER COLUMN id SET DEFAULT nextval('public.badges_batch_id_seq'::regclass);


--
-- Name: core_carouselslide id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_carouselslide ALTER COLUMN id SET DEFAULT nextval('public.core_carouselslide_id_seq'::regclass);


--
-- Name: core_emailverificationtoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_emailverificationtoken ALTER COLUMN id SET DEFAULT nextval('public.core_emailverificationtoken_id_seq'::regclass);


--
-- Name: core_event id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_event ALTER COLUMN id SET DEFAULT nextval('public.core_event_id_seq'::regclass);


--
-- Name: core_organization id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_organization ALTER COLUMN id SET DEFAULT nextval('public.core_organization_id_seq'::regclass);


--
-- Name: core_passwordresettoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_passwordresettoken ALTER COLUMN id SET DEFAULT nextval('public.core_passwordresettoken_id_seq'::regclass);


--
-- Name: core_person id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_person ALTER COLUMN id SET DEFAULT nextval('public.core_person_id_seq'::regclass);


--
-- Name: core_venue id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_venue ALTER COLUMN id SET DEFAULT nextval('public.core_venue_id_seq'::regclass);


--
-- Name: desucon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.desucon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: desucon2016_signupextrav2 id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2 ALTER COLUMN id SET DEFAULT nextval('public.desucon2016_signupextrav2_id_seq'::regclass);


--
-- Name: desucon2016_signupextrav2_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2_special_diet ALTER COLUMN id SET DEFAULT nextval('public.desucon2016_signupextrav2_special_diet_id_seq'::regclass);


--
-- Name: desucon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.desucon2016_specialdiet_id_seq'::regclass);


--
-- Name: desucon2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.desucon2017_signupextra_id_seq'::regclass);


--
-- Name: desucon2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.desucon2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: desucon2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.desucon2017_specialdiet_id_seq'::regclass);


--
-- Name: desucon2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.desucon2018_signupextra_id_seq'::regclass);


--
-- Name: desucon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.desucon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: desucon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.desucon2018_specialdiet_id_seq'::regclass);


--
-- Name: desucon2019_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra ALTER COLUMN id SET DEFAULT nextval('public.desucon2019_signupextra_id_seq'::regclass);


--
-- Name: desucon2019_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.desucon2019_signupextra_special_diet_id_seq'::regclass);


--
-- Name: desucon2019_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.desucon2019_specialdiet_id_seq'::regclass);


--
-- Name: desuprofile_integration_confirmationcode id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_confirmationcode ALTER COLUMN id SET DEFAULT nextval('public.desuprofile_integration_confirmationcode_id_seq'::regclass);


--
-- Name: directory_directoryaccessgroup id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryaccessgroup ALTER COLUMN id SET DEFAULT nextval('public.directory_directoryaccessgroup_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: django_site id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);


--
-- Name: enrollment_conconpart id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_conconpart ALTER COLUMN id SET DEFAULT nextval('public.enrollment_conconpart_id_seq'::regclass);


--
-- Name: enrollment_enrollment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment ALTER COLUMN id SET DEFAULT nextval('public.enrollment_enrollment_id_seq'::regclass);


--
-- Name: enrollment_enrollment_concon_parts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_concon_parts ALTER COLUMN id SET DEFAULT nextval('public.enrollment_enrollment_concon_parts_id_seq'::regclass);


--
-- Name: enrollment_enrollment_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_special_diet ALTER COLUMN id SET DEFAULT nextval('public.enrollment_enrollment_special_diet_id_seq'::regclass);


--
-- Name: enrollment_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.enrollment_specialdiet_id_seq'::regclass);


--
-- Name: event_log_entry id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry ALTER COLUMN id SET DEFAULT nextval('public.event_log_entry_id_seq'::regclass);


--
-- Name: event_log_subscription id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_subscription ALTER COLUMN id SET DEFAULT nextval('public.event_log_subscription_id_seq'::regclass);


--
-- Name: feedback_feedbackmessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feedback_feedbackmessage ALTER COLUMN id SET DEFAULT nextval('public.feedback_feedbackmessage_id_seq'::regclass);


--
-- Name: finncon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.finncon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: finncon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.finncon2016_specialdiet_id_seq'::regclass);


--
-- Name: finncon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.finncon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: finncon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.finncon2018_specialdiet_id_seq'::regclass);


--
-- Name: frostbite2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.frostbite2017_signupextra_id_seq'::regclass);


--
-- Name: frostbite2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: frostbite2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2017_specialdiet_id_seq'::regclass);


--
-- Name: frostbite2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.frostbite2018_signupextra_id_seq'::regclass);


--
-- Name: frostbite2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: frostbite2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2018_specialdiet_id_seq'::regclass);


--
-- Name: frostbite2019_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra ALTER COLUMN id SET DEFAULT nextval('public.frostbite2019_signupextra_id_seq'::regclass);


--
-- Name: frostbite2019_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2019_signupextra_special_diet_id_seq'::regclass);


--
-- Name: frostbite2019_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.frostbite2019_specialdiet_id_seq'::regclass);


--
-- Name: hitpoint2015_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.hitpoint2015_signupextra_special_diet_id_seq'::regclass);


--
-- Name: hitpoint2015_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.hitpoint2015_specialdiet_id_seq'::regclass);


--
-- Name: hitpoint2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.hitpoint2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: hitpoint2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.hitpoint2017_specialdiet_id_seq'::regclass);


--
-- Name: hitpoint2017_timeslot id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_timeslot ALTER COLUMN id SET DEFAULT nextval('public.hitpoint2017_timeslot_id_seq'::regclass);


--
-- Name: intra_team id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_team ALTER COLUMN id SET DEFAULT nextval('public.intra_team_id_seq'::regclass);


--
-- Name: intra_teammember id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_teammember ALTER COLUMN id SET DEFAULT nextval('public.intra_teammember_id_seq'::regclass);


--
-- Name: kawacon2016_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_night ALTER COLUMN id SET DEFAULT nextval('public.kawacon2016_night_id_seq'::regclass);


--
-- Name: kawacon2016_signupextra_needs_lodging id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_needs_lodging ALTER COLUMN id SET DEFAULT nextval('public.kawacon2016_signupextra_needs_lodging_id_seq'::regclass);


--
-- Name: kawacon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kawacon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kawacon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kawacon2016_specialdiet_id_seq'::regclass);


--
-- Name: kawacon2017_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_night ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_night_id_seq'::regclass);


--
-- Name: kawacon2017_shift id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_shift ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_shift_id_seq'::regclass);


--
-- Name: kawacon2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_signupextra_id_seq'::regclass);


--
-- Name: kawacon2017_signupextra_needs_lodging id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_needs_lodging ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_signupextra_needs_lodging_id_seq'::regclass);


--
-- Name: kawacon2017_signupextra_shifts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_shifts ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_signupextra_shifts_id_seq'::regclass);


--
-- Name: kawacon2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kawacon2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kawacon2017_specialdiet_id_seq'::regclass);


--
-- Name: kuplii2015_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2015_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kuplii2015_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2015_specialdiet_id_seq'::regclass);


--
-- Name: kuplii2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kuplii2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2016_specialdiet_id_seq'::regclass);


--
-- Name: kuplii2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.kuplii2017_signupextra_id_seq'::regclass);


--
-- Name: kuplii2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kuplii2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2017_specialdiet_id_seq'::regclass);


--
-- Name: kuplii2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.kuplii2018_signupextra_id_seq'::regclass);


--
-- Name: kuplii2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: kuplii2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.kuplii2018_specialdiet_id_seq'::regclass);


--
-- Name: labour_alternativesignupform id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_alternativesignupform ALTER COLUMN id SET DEFAULT nextval('public.labour_alternativesignupform_id_seq'::regclass);


--
-- Name: labour_emptysignupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_emptysignupextra ALTER COLUMN id SET DEFAULT nextval('public.labour_emptysignupextra_id_seq'::regclass);


--
-- Name: labour_infolink id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_infolink ALTER COLUMN id SET DEFAULT nextval('public.labour_infolink_id_seq'::regclass);


--
-- Name: labour_job id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_job ALTER COLUMN id SET DEFAULT nextval('public.labour_job_id_seq'::regclass);


--
-- Name: labour_jobcategory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory ALTER COLUMN id SET DEFAULT nextval('public.labour_jobcategory_id_seq'::regclass);


--
-- Name: labour_jobcategory_personnel_classes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_personnel_classes ALTER COLUMN id SET DEFAULT nextval('public.labour_jobcategory_personnel_classes_id_seq'::regclass);


--
-- Name: labour_jobcategory_required_qualifications id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_required_qualifications ALTER COLUMN id SET DEFAULT nextval('public.labour_jobcategory_required_qualifications_id_seq'::regclass);


--
-- Name: labour_jobrequirement id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobrequirement ALTER COLUMN id SET DEFAULT nextval('public.labour_jobrequirement_id_seq'::regclass);


--
-- Name: labour_perk id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_perk ALTER COLUMN id SET DEFAULT nextval('public.labour_perk_id_seq'::regclass);


--
-- Name: labour_personnelclass id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass ALTER COLUMN id SET DEFAULT nextval('public.labour_personnelclass_id_seq'::regclass);


--
-- Name: labour_personnelclass_perks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass_perks ALTER COLUMN id SET DEFAULT nextval('public.labour_personnelclass_perks_id_seq'::regclass);


--
-- Name: labour_personqualification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personqualification ALTER COLUMN id SET DEFAULT nextval('public.labour_personqualification_id_seq'::regclass);


--
-- Name: labour_qualification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_qualification ALTER COLUMN id SET DEFAULT nextval('public.labour_qualification_id_seq'::regclass);


--
-- Name: labour_shift id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_shift ALTER COLUMN id SET DEFAULT nextval('public.labour_shift_id_seq'::regclass);


--
-- Name: labour_signup id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup ALTER COLUMN id SET DEFAULT nextval('public.labour_signup_id_seq'::regclass);


--
-- Name: labour_signup_job_categories id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories ALTER COLUMN id SET DEFAULT nextval('public.labour_signup_job_categories_id_seq'::regclass);


--
-- Name: labour_signup_job_categories_accepted id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_accepted ALTER COLUMN id SET DEFAULT nextval('public.labour_signup_job_categories_accepted_id_seq'::regclass);


--
-- Name: labour_signup_job_categories_rejected id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_rejected ALTER COLUMN id SET DEFAULT nextval('public.labour_signup_job_categories_rejected_id_seq'::regclass);


--
-- Name: labour_signup_personnel_classes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_personnel_classes ALTER COLUMN id SET DEFAULT nextval('public.labour_signup_personnel_classes_id_seq'::regclass);


--
-- Name: labour_survey id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_survey ALTER COLUMN id SET DEFAULT nextval('public.labour_survey_id_seq'::regclass);


--
-- Name: labour_surveyrecord id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_surveyrecord ALTER COLUMN id SET DEFAULT nextval('public.labour_surveyrecord_id_seq'::regclass);


--
-- Name: labour_workperiod id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_workperiod ALTER COLUMN id SET DEFAULT nextval('public.labour_workperiod_id_seq'::regclass);


--
-- Name: lakeuscon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.lakeuscon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: lakeuscon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.lakeuscon2016_specialdiet_id_seq'::regclass);


--
-- Name: lippukala_code id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_code ALTER COLUMN id SET DEFAULT nextval('public.lippukala_code_id_seq'::regclass);


--
-- Name: lippukala_order id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_order ALTER COLUMN id SET DEFAULT nextval('public.lippukala_order_id_seq'::regclass);


--
-- Name: listings_externalevent id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_externalevent ALTER COLUMN id SET DEFAULT nextval('public.listings_externalevent_id_seq'::regclass);


--
-- Name: listings_listing id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing ALTER COLUMN id SET DEFAULT nextval('public.listings_listing_id_seq'::regclass);


--
-- Name: listings_listing_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_events ALTER COLUMN id SET DEFAULT nextval('public.listings_listing_events_id_seq'::regclass);


--
-- Name: listings_listing_external_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_external_events ALTER COLUMN id SET DEFAULT nextval('public.listings_listing_external_events_id_seq'::regclass);


--
-- Name: mailings_message id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_message ALTER COLUMN id SET DEFAULT nextval('public.mailings_message_id_seq'::regclass);


--
-- Name: mailings_personmessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage ALTER COLUMN id SET DEFAULT nextval('public.mailings_personmessage_id_seq'::regclass);


--
-- Name: mailings_personmessagebody id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessagebody ALTER COLUMN id SET DEFAULT nextval('public.mailings_personmessagebody_id_seq'::regclass);


--
-- Name: mailings_personmessagesubject id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessagesubject ALTER COLUMN id SET DEFAULT nextval('public.mailings_personmessagesubject_id_seq'::regclass);


--
-- Name: mailings_recipientgroup id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup ALTER COLUMN id SET DEFAULT nextval('public.mailings_recipientgroup_id_seq'::regclass);


--
-- Name: matsucon2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.matsucon2018_signupextra_id_seq'::regclass);


--
-- Name: matsucon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.matsucon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: membership_membership id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membership ALTER COLUMN id SET DEFAULT nextval('public.membership_membership_id_seq'::regclass);


--
-- Name: membership_membershipfeepayment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershipfeepayment ALTER COLUMN id SET DEFAULT nextval('public.membership_membershipfeepayment_id_seq'::regclass);


--
-- Name: membership_term id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_term ALTER COLUMN id SET DEFAULT nextval('public.membership_term_id_seq'::regclass);


--
-- Name: mimicon2016_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_night ALTER COLUMN id SET DEFAULT nextval('public.mimicon2016_night_id_seq'::regclass);


--
-- Name: mimicon2016_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.mimicon2016_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: mimicon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.mimicon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: mimicon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.mimicon2016_specialdiet_id_seq'::regclass);


--
-- Name: mimicon2018_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_night ALTER COLUMN id SET DEFAULT nextval('public.mimicon2018_night_id_seq'::regclass);


--
-- Name: mimicon2018_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.mimicon2018_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: mimicon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.mimicon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: mimicon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.mimicon2018_specialdiet_id_seq'::regclass);


--
-- Name: nexmo_deliverystatusfragment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_deliverystatusfragment ALTER COLUMN id SET DEFAULT nextval('public.nexmo_deliverystatusfragment_id_seq'::regclass);


--
-- Name: nexmo_inboundmessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_inboundmessage ALTER COLUMN id SET DEFAULT nextval('public.nexmo_inboundmessage_id_seq'::regclass);


--
-- Name: nexmo_inboundmessagefragment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_inboundmessagefragment ALTER COLUMN id SET DEFAULT nextval('public.nexmo_inboundmessagefragment_id_seq'::regclass);


--
-- Name: nexmo_outboundmessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_outboundmessage ALTER COLUMN id SET DEFAULT nextval('public.nexmo_outboundmessage_id_seq'::regclass);


--
-- Name: nippori2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nippori2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.nippori2017_signupextra_id_seq'::regclass);


--
-- Name: oauth2_provider_accesstoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken ALTER COLUMN id SET DEFAULT nextval('public.oauth2_provider_accesstoken_id_seq'::regclass);


--
-- Name: oauth2_provider_application id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_application ALTER COLUMN id SET DEFAULT nextval('public.oauth2_provider_application_id_seq'::regclass);


--
-- Name: oauth2_provider_grant id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_grant ALTER COLUMN id SET DEFAULT nextval('public.oauth2_provider_grant_id_seq'::regclass);


--
-- Name: oauth2_provider_refreshtoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken ALTER COLUMN id SET DEFAULT nextval('public.oauth2_provider_refreshtoken_id_seq'::regclass);


--
-- Name: payments_payment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_payment ALTER COLUMN id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);


--
-- Name: popcult2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.popcult2017_signupextra_id_seq'::regclass);


--
-- Name: popcult2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.popcult2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: popcultday2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.popcultday2018_signupextra_id_seq'::regclass);


--
-- Name: popcultday2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.popcultday2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: programme_alternativeprogrammeform id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_alternativeprogrammeform ALTER COLUMN id SET DEFAULT nextval('public.programme_alternativeprogrammeform_id_seq'::regclass);


--
-- Name: programme_category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_category ALTER COLUMN id SET DEFAULT nextval('public.programme_category_id_seq'::regclass);


--
-- Name: programme_freeformorganizer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_freeformorganizer ALTER COLUMN id SET DEFAULT nextval('public.programme_freeformorganizer_id_seq'::regclass);


--
-- Name: programme_invitation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation ALTER COLUMN id SET DEFAULT nextval('public.programme_invitation_id_seq'::regclass);


--
-- Name: programme_programme id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme ALTER COLUMN id SET DEFAULT nextval('public.programme_programme_id_seq'::regclass);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_hitpoint2017_preferred_time_slots ALTER COLUMN id SET DEFAULT nextval('public.programme_programme_hitpoint2017_preferred_time_slots_id_seq'::regclass);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_ropecon2018_preferred_time_slots ALTER COLUMN id SET DEFAULT nextval('public.programme_programme_ropecon2018_preferred_time_slots_id_seq'::regclass);


--
-- Name: programme_programme_tags id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_tags ALTER COLUMN id SET DEFAULT nextval('public.programme_programme_tags_id_seq'::regclass);


--
-- Name: programme_programmefeedback id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmefeedback ALTER COLUMN id SET DEFAULT nextval('public.programme_programmefeedback_id_seq'::regclass);


--
-- Name: programme_programmerole id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole ALTER COLUMN id SET DEFAULT nextval('public.programme_programmerole_id_seq'::regclass);


--
-- Name: programme_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_role ALTER COLUMN id SET DEFAULT nextval('public.programme_role_id_seq'::regclass);


--
-- Name: programme_room id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_room ALTER COLUMN id SET DEFAULT nextval('public.programme_room_id_seq'::regclass);


--
-- Name: programme_specialstarttime id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_specialstarttime ALTER COLUMN id SET DEFAULT nextval('public.programme_specialstarttime_id_seq'::regclass);


--
-- Name: programme_tag id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_tag ALTER COLUMN id SET DEFAULT nextval('public.programme_tag_id_seq'::regclass);


--
-- Name: programme_timeblock id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_timeblock ALTER COLUMN id SET DEFAULT nextval('public.programme_timeblock_id_seq'::regclass);


--
-- Name: programme_view id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_view ALTER COLUMN id SET DEFAULT nextval('public.programme_view_id_seq'::regclass);


--
-- Name: programme_viewroom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_viewroom ALTER COLUMN id SET DEFAULT nextval('public.programme_viewroom_id_seq'::regclass);


--
-- Name: ropecon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.ropecon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: ropecon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.ropecon2018_specialdiet_id_seq'::regclass);


--
-- Name: ropecon2018_timeslot id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_timeslot ALTER COLUMN id SET DEFAULT nextval('public.ropecon2018_timeslot_id_seq'::regclass);


--
-- Name: shippocon2016_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra ALTER COLUMN id SET DEFAULT nextval('public.shippocon2016_signupextra_id_seq'::regclass);


--
-- Name: shippocon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.shippocon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: shippocon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.shippocon2016_specialdiet_id_seq'::regclass);


--
-- Name: sms_hotword id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_hotword ALTER COLUMN id SET DEFAULT nextval('public.sms_hotword_id_seq'::regclass);


--
-- Name: sms_nominee id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee ALTER COLUMN id SET DEFAULT nextval('public.sms_nominee_id_seq'::regclass);


--
-- Name: sms_nominee_category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee_category ALTER COLUMN id SET DEFAULT nextval('public.sms_nominee_category_id_seq'::regclass);


--
-- Name: sms_smsmessagein id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessagein ALTER COLUMN id SET DEFAULT nextval('public.sms_smsmessagein_id_seq'::regclass);


--
-- Name: sms_smsmessageout id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessageout ALTER COLUMN id SET DEFAULT nextval('public.sms_smsmessageout_id_seq'::regclass);


--
-- Name: sms_vote id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_vote ALTER COLUMN id SET DEFAULT nextval('public.sms_vote_id_seq'::regclass);


--
-- Name: sms_votecategory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_votecategory ALTER COLUMN id SET DEFAULT nextval('public.sms_votecategory_id_seq'::regclass);


--
-- Name: surveys_eventsurvey id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurvey ALTER COLUMN id SET DEFAULT nextval('public.surveys_eventsurvey_id_seq'::regclass);


--
-- Name: surveys_eventsurveyresult id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurveyresult ALTER COLUMN id SET DEFAULT nextval('public.surveys_eventsurveyresult_id_seq'::regclass);


--
-- Name: surveys_globalsurvey id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurvey ALTER COLUMN id SET DEFAULT nextval('public.surveys_globalsurvey_id_seq'::regclass);


--
-- Name: surveys_globalsurveyresult id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurveyresult ALTER COLUMN id SET DEFAULT nextval('public.surveys_globalsurveyresult_id_seq'::regclass);


--
-- Name: tickets_accommodationinformation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation ALTER COLUMN id SET DEFAULT nextval('public.tickets_accommodationinformation_id_seq'::regclass);


--
-- Name: tickets_accommodationinformation_limit_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation_limit_groups ALTER COLUMN id SET DEFAULT nextval('public.tickets_accommodationinformation_limit_groups_id_seq'::regclass);


--
-- Name: tickets_batch id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_batch ALTER COLUMN id SET DEFAULT nextval('public.tickets_batch_id_seq'::regclass);


--
-- Name: tickets_customer id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_customer ALTER COLUMN id SET DEFAULT nextval('public.tickets_customer_id_seq'::regclass);


--
-- Name: tickets_limitgroup id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_limitgroup ALTER COLUMN id SET DEFAULT nextval('public.tickets_limitgroup_id_seq'::regclass);


--
-- Name: tickets_order id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order ALTER COLUMN id SET DEFAULT nextval('public.tickets_order_id_seq'::regclass);


--
-- Name: tickets_orderproduct id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_orderproduct ALTER COLUMN id SET DEFAULT nextval('public.tickets_orderproduct_id_seq'::regclass);


--
-- Name: tickets_product id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product ALTER COLUMN id SET DEFAULT nextval('public.tickets_product_id_seq'::regclass);


--
-- Name: tickets_product_limit_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product_limit_groups ALTER COLUMN id SET DEFAULT nextval('public.tickets_product_limit_groups_id_seq'::regclass);


--
-- Name: tickets_shirtorder id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtorder ALTER COLUMN id SET DEFAULT nextval('public.tickets_shirtorder_id_seq'::regclass);


--
-- Name: tickets_shirtsize id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtsize ALTER COLUMN id SET DEFAULT nextval('public.tickets_shirtsize_id_seq'::regclass);


--
-- Name: tickets_shirttype id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirttype ALTER COLUMN id SET DEFAULT nextval('public.tickets_shirttype_id_seq'::regclass);


--
-- Name: tracon11_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_night ALTER COLUMN id SET DEFAULT nextval('public.tracon11_night_id_seq'::regclass);


--
-- Name: tracon11_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.tracon11_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: tracon11_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tracon11_signupextra_special_diet_id_seq'::regclass);


--
-- Name: tracon11_signupextrav2 id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2 ALTER COLUMN id SET DEFAULT nextval('public.tracon11_signupextrav2_id_seq'::regclass);


--
-- Name: tracon11_signupextrav2_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.tracon11_signupextrav2_lodging_needs_id_seq'::regclass);


--
-- Name: tracon11_signupextrav2_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tracon11_signupextrav2_special_diet_id_seq'::regclass);


--
-- Name: tracon11_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.tracon11_specialdiet_id_seq'::regclass);


--
-- Name: tracon2017_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_night ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_night_id_seq'::regclass);


--
-- Name: tracon2017_poison id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_poison ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_poison_id_seq'::regclass);


--
-- Name: tracon2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_signupextra_id_seq'::regclass);


--
-- Name: tracon2017_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: tracon2017_signupextra_pick_your_poison id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_pick_your_poison ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_signupextra_pick_your_poison_id_seq'::regclass);


--
-- Name: tracon2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tracon2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: tracon2018_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_night ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_night_id_seq'::regclass);


--
-- Name: tracon2018_poison id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_poison ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_poison_id_seq'::regclass);


--
-- Name: tracon2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_signupextra_id_seq'::regclass);


--
-- Name: tracon2018_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: tracon2018_signupextra_pick_your_poison id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_pick_your_poison ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_signupextra_pick_your_poison_id_seq'::regclass);


--
-- Name: tracon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tracon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: tracon9_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_night ALTER COLUMN id SET DEFAULT nextval('public.tracon9_night_id_seq'::regclass);


--
-- Name: tracon9_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.tracon9_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: tracon9_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tracon9_signupextra_special_diet_id_seq'::regclass);


--
-- Name: tracon9_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.tracon9_specialdiet_id_seq'::regclass);


--
-- Name: traconx_night id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_night ALTER COLUMN id SET DEFAULT nextval('public.traconx_night_id_seq'::regclass);


--
-- Name: traconx_signupextra_lodging_needs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_lodging_needs ALTER COLUMN id SET DEFAULT nextval('public.traconx_signupextra_lodging_needs_id_seq'::regclass);


--
-- Name: traconx_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.traconx_signupextra_special_diet_id_seq'::regclass);


--
-- Name: traconx_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.traconx_specialdiet_id_seq'::regclass);


--
-- Name: tylycon2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.tylycon2017_signupextra_id_seq'::regclass);


--
-- Name: tylycon2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.tylycon2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: tylycon2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.tylycon2017_specialdiet_id_seq'::regclass);


--
-- Name: worldcon75_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra ALTER COLUMN id SET DEFAULT nextval('public.worldcon75_signupextra_id_seq'::regclass);


--
-- Name: worldcon75_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.worldcon75_signupextra_special_diet_id_seq'::regclass);


--
-- Name: yukicon2016_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2016_signupextra_special_diet_id_seq'::regclass);


--
-- Name: yukicon2016_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2016_specialdiet_id_seq'::regclass);


--
-- Name: yukicon2017_eventday id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_eventday ALTER COLUMN id SET DEFAULT nextval('public.yukicon2017_eventday_id_seq'::regclass);


--
-- Name: yukicon2017_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra ALTER COLUMN id SET DEFAULT nextval('public.yukicon2017_signupextra_id_seq'::regclass);


--
-- Name: yukicon2017_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2017_signupextra_special_diet_id_seq'::regclass);


--
-- Name: yukicon2017_signupextra_work_days id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_work_days ALTER COLUMN id SET DEFAULT nextval('public.yukicon2017_signupextra_work_days_id_seq'::regclass);


--
-- Name: yukicon2017_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2017_specialdiet_id_seq'::regclass);


--
-- Name: yukicon2018_eventday id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_eventday ALTER COLUMN id SET DEFAULT nextval('public.yukicon2018_eventday_id_seq'::regclass);


--
-- Name: yukicon2018_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra ALTER COLUMN id SET DEFAULT nextval('public.yukicon2018_signupextra_id_seq'::regclass);


--
-- Name: yukicon2018_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2018_signupextra_special_diet_id_seq'::regclass);


--
-- Name: yukicon2018_signupextra_work_days id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_work_days ALTER COLUMN id SET DEFAULT nextval('public.yukicon2018_signupextra_work_days_id_seq'::regclass);


--
-- Name: yukicon2018_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2018_specialdiet_id_seq'::regclass);


--
-- Name: yukicon2019_eventday id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_eventday ALTER COLUMN id SET DEFAULT nextval('public.yukicon2019_eventday_id_seq'::regclass);


--
-- Name: yukicon2019_signupextra id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra ALTER COLUMN id SET DEFAULT nextval('public.yukicon2019_signupextra_id_seq'::regclass);


--
-- Name: yukicon2019_signupextra_special_diet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_special_diet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2019_signupextra_special_diet_id_seq'::regclass);


--
-- Name: yukicon2019_signupextra_work_days id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_work_days ALTER COLUMN id SET DEFAULT nextval('public.yukicon2019_signupextra_work_days_id_seq'::regclass);


--
-- Name: yukicon2019_specialdiet id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_specialdiet ALTER COLUMN id SET DEFAULT nextval('public.yukicon2019_specialdiet_id_seq'::regclass);


--
-- Data for Name: access_accessorganizationmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_accessorganizationmeta (organization_id, admin_group_id) FROM stdin;
\.


--
-- Data for Name: access_emailalias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_emailalias (id, account_name, email_address, created_at, modified_at, domain_id, group_grant_id, person_id, type_id) FROM stdin;
\.


--
-- Data for Name: access_emailaliasdomain; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_emailaliasdomain (id, domain_name, organization_id, has_internal_aliases) FROM stdin;
\.


--
-- Data for Name: access_emailaliastype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_emailaliastype (id, metavar, account_name_code, domain_id, priority) FROM stdin;
\.


--
-- Data for Name: access_grantedprivilege; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_grantedprivilege (id, granted_at, person_id, privilege_id, state) FROM stdin;
\.


--
-- Data for Name: access_groupemailaliasgrant; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_groupemailaliasgrant (id, group_id, type_id, active_until) FROM stdin;
\.


--
-- Data for Name: access_groupprivilege; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_groupprivilege (id, event_id, group_id, privilege_id) FROM stdin;
\.


--
-- Data for Name: access_internalemailalias; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_internalemailalias (id, account_name, target_emails, email_address, app_label, created_at, modified_at, domain_id, event_id) FROM stdin;
\.


--
-- Data for Name: access_privilege; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_privilege (id, slug, title, description, request_success_message, grant_code, disclaimers) FROM stdin;
\.


--
-- Data for Name: access_slackaccess; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_slackaccess (id, team_name, api_token, privilege_id) FROM stdin;
\.


--
-- Data for Name: access_smtppassword; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_smtppassword (id, password_hash, created_at, person_id, smtp_server_id) FROM stdin;
\.


--
-- Data for Name: access_smtpserver; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_smtpserver (id, hostname, crypto, port) FROM stdin;
\.


--
-- Data for Name: access_smtpserver_domains; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.access_smtpserver_domains (id, smtpserver_id, emailaliasdomain_id) FROM stdin;
\.


--
-- Data for Name: aicon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2016_signupextra (signup_id, shift_type, total_work, want_certificate, certificate_delivery_address, special_diet_other, need_lodging, prior_experience, free_text, email_alias, is_active) FROM stdin;
\.


--
-- Data for Name: aicon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: aicon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: aicon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2018_signupextra (signup_id, is_active, shift_type, total_work, want_certificate, certificate_delivery_address, special_diet_other, need_lodging, prior_experience, free_text, email_alias) FROM stdin;
\.


--
-- Data for Name: aicon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: aicon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.aicon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: animecon2015_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2015_night (id, name) FROM stdin;
\.


--
-- Data for Name: animecon2015_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2015_signupextra (signup_id, total_work, want_certificate, certificate_delivery_address, special_diet_other, prior_experience, free_text, personal_identification_number, is_active) FROM stdin;
\.


--
-- Data for Name: animecon2015_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2015_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: animecon2015_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2015_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: animecon2015_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2015_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: animecon2016_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2016_night (id, name) FROM stdin;
\.


--
-- Data for Name: animecon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2016_signupextra (signup_id, total_work, personal_identification_number, want_certificate, certificate_delivery_address, special_diet_other, prior_experience, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: animecon2016_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2016_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: animecon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: animecon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.animecon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add user	2	add_user
5	Can change user	2	change_user
6	Can delete user	2	delete_user
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add site	6	add_site
17	Can change site	6	change_site
18	Can delete site	6	delete_site
19	Can add log entry	7	add_logentry
20	Can change log entry	7	change_logentry
21	Can delete log entry	7	delete_logentry
22	Can add refresh token	8	add_refreshtoken
23	Can change refresh token	8	change_refreshtoken
24	Can delete refresh token	8	delete_refreshtoken
25	Can add access token	9	add_accesstoken
26	Can change access token	9	change_accesstoken
27	Can delete access token	9	delete_accesstoken
28	Can add grant	10	add_grant
29	Can change grant	10	change_grant
30	Can delete grant	10	delete_grant
31	Can add application	11	add_application
32	Can change application	11	change_application
33	Can delete application	11	delete_application
34	Can add Inbound Message Fragment	12	add_inboundmessagefragment
35	Can change Inbound Message Fragment	12	change_inboundmessagefragment
36	Can delete Inbound Message Fragment	12	delete_inboundmessagefragment
37	Can add Inbound Message	13	add_inboundmessage
38	Can change Inbound Message	13	change_inboundmessage
39	Can delete Inbound Message	13	delete_inboundmessage
40	Can add delivery status fragment	14	add_deliverystatusfragment
41	Can change delivery status fragment	14	change_deliverystatusfragment
42	Can delete delivery status fragment	14	delete_deliverystatusfragment
43	Can add Outbound Message	15	add_outboundmessage
44	Can change Outbound Message	15	change_outboundmessage
45	Can delete Outbound Message	15	delete_outboundmessage
46	Can add carousel slide	16	add_carouselslide
47	Can change carousel slide	16	change_carouselslide
48	Can delete carousel slide	16	delete_carouselslide
49	Can add Henkilö	17	add_person
50	Can change Henkilö	17	change_person
51	Can delete Henkilö	17	delete_person
52	Can add Organisaatio	18	add_organization
53	Can change Organisaatio	18	change_organization
54	Can delete Organisaatio	18	delete_organization
55	Can add Tapahtumapaikka	19	add_venue
56	Can change Tapahtumapaikka	19	change_venue
57	Can delete Tapahtumapaikka	19	delete_venue
58	Can add password reset token	20	add_passwordresettoken
59	Can change password reset token	20	change_passwordresettoken
60	Can delete password reset token	20	delete_passwordresettoken
61	Can add email verification token	21	add_emailverificationtoken
62	Can change email verification token	21	change_emailverificationtoken
63	Can delete email verification token	21	delete_emailverificationtoken
64	Can add Tapahtuma	22	add_event
65	Can change Tapahtuma	22	change_event
66	Can delete Tapahtuma	22	delete_event
67	Can add special start time	23	add_specialstarttime
68	Can change special start time	23	change_specialstarttime
69	Can delete special start time	23	delete_specialstarttime
70	Can add category	24	add_category
71	Can change category	24	change_category
72	Can delete category	24	delete_category
73	Can add role	25	add_role
74	Can change role	25	change_role
75	Can delete role	25	delete_role
76	Can add tag	26	add_tag
77	Can change tag	26	change_tag
78	Can delete tag	26	delete_tag
79	Can add freeform organizer	27	add_freeformorganizer
80	Can change freeform organizer	27	change_freeformorganizer
81	Can delete freeform organizer	27	delete_freeformorganizer
82	Can add invitation	28	add_invitation
83	Can change invitation	28	change_invitation
84	Can delete invitation	28	delete_invitation
85	Can add programme feedback	29	add_programmefeedback
86	Can change programme feedback	29	change_programmefeedback
87	Can delete programme feedback	29	delete_programmefeedback
88	Can add alternative programme form	30	add_alternativeprogrammeform
89	Can change alternative programme form	30	change_alternativeprogrammeform
90	Can delete alternative programme form	30	delete_alternativeprogrammeform
91	Can add schedule view	31	add_view
92	Can change schedule view	31	change_view
93	Can delete schedule view	31	delete_view
94	Can add invitation	28	add_invitationadminproxy
95	Can change invitation	28	change_invitationadminproxy
96	Can delete invitation	28	delete_invitationadminproxy
97	Can add programme event meta	32	add_programmeeventmeta
98	Can change programme event meta	32	change_programmeeventmeta
99	Can delete programme event meta	32	delete_programmeeventmeta
100	Can add time block	33	add_timeblock
101	Can change time block	33	change_timeblock
102	Can delete time block	33	delete_timeblock
103	Can add Programme host	34	add_programmerole
104	Can change Programme host	34	change_programmerole
105	Can delete Programme host	34	delete_programmerole
106	Can add programme	35	add_programme
107	Can change programme	35	change_programme
108	Can delete programme	35	delete_programme
109	Can add cold offers programme event meta proxy	32	add_coldoffersprogrammeeventmetaproxy
110	Can change cold offers programme event meta proxy	32	change_coldoffersprogrammeeventmetaproxy
111	Can delete cold offers programme event meta proxy	32	delete_coldoffersprogrammeeventmetaproxy
112	Can add Room	36	add_room
113	Can change Room	36	change_room
114	Can delete Room	36	delete_room
115	Can add programme management proxy	35	add_programmemanagementproxy
116	Can change programme management proxy	35	change_programmemanagementproxy
117	Can delete programme management proxy	35	delete_programmemanagementproxy
118	Can add freeform organizer	27	add_freeformorganizeradminproxy
119	Can change freeform organizer	27	change_freeformorganizeradminproxy
120	Can delete freeform organizer	27	delete_freeformorganizeradminproxy
121	Can add signup	41	add_signup
122	Can change signup	41	change_signup
123	Can delete signup	41	delete_signup
124	Can add perk	42	add_perk
125	Can change perk	42	change_perk
126	Can delete perk	42	delete_perk
127	Can add obsolete empty signup extra v1	43	add_obsoleteemptysignupextrav1
128	Can change obsolete empty signup extra v1	43	change_obsoleteemptysignupextrav1
129	Can delete obsolete empty signup extra v1	43	delete_obsoleteemptysignupextrav1
130	Can add job requirement	44	add_jobrequirement
131	Can change job requirement	44	change_jobrequirement
132	Can delete job requirement	44	delete_jobrequirement
133	Can add shift	45	add_shift
134	Can change shift	45	change_shift
135	Can delete shift	45	delete_shift
136	Can add qualification	46	add_qualification
137	Can change qualification	46	change_qualification
138	Can delete qualification	46	delete_qualification
139	Can add alternative signup form	47	add_alternativesignupform
140	Can change alternative signup form	47	change_alternativesignupform
141	Can delete alternative signup form	47	delete_alternativesignupform
142	Can add job category	48	add_jobcategory
143	Can change job category	48	change_jobcategory
144	Can delete job category	48	delete_jobcategory
145	Can add job	49	add_job
146	Can change job	49	change_job
147	Can delete job	49	delete_job
148	Can add info link	50	add_infolink
149	Can change info link	50	change_infolink
150	Can delete info link	50	delete_infolink
151	Can add qualification holder	51	add_personqualification
152	Can change qualification holder	51	change_personqualification
153	Can delete qualification holder	51	delete_personqualification
154	Can add signup certificate proxy	41	add_signupcertificateproxy
155	Can change signup certificate proxy	41	change_signupcertificateproxy
156	Can delete signup certificate proxy	41	delete_signupcertificateproxy
157	Can add Survey	52	add_survey
158	Can change Survey	52	change_survey
159	Can delete Survey	52	delete_survey
160	Can add survey record	53	add_surveyrecord
161	Can change survey record	53	change_surveyrecord
162	Can delete survey record	53	delete_surveyrecord
163	Can add job category management proxy	48	add_jobcategorymanagementproxy
164	Can change job category management proxy	48	change_jobcategorymanagementproxy
165	Can delete job category management proxy	48	delete_jobcategorymanagementproxy
166	Can add signup onboarding proxy	41	add_signuponboardingproxy
167	Can change signup onboarding proxy	41	change_signuponboardingproxy
168	Can delete signup onboarding proxy	41	delete_signuponboardingproxy
169	Can add work period	54	add_workperiod
170	Can change work period	54	change_workperiod
171	Can delete work period	54	delete_workperiod
172	Can add labour event meta	55	add_laboureventmeta
173	Can change labour event meta	55	change_laboureventmeta
174	Can delete labour event meta	55	delete_laboureventmeta
175	Can add empty signup extra	56	add_emptysignupextra
176	Can change empty signup extra	56	change_emptysignupextra
177	Can delete empty signup extra	56	delete_emptysignupextra
178	Can add personnel class	57	add_personnelclass
179	Can change personnel class	57	change_personnelclass
180	Can delete personnel class	57	delete_personnelclass
181	Can add JV-kortti	61	add_jvkortti
182	Can change JV-kortti	61	change_jvkortti
183	Can delete JV-kortti	61	delete_jvkortti
184	Can add tilaus	62	add_order
185	Can change tilaus	62	change_order
186	Can delete tilaus	62	delete_order
187	Can add majoittujan tiedot	63	add_accommodationinformation
188	Can change majoittujan tiedot	63	change_accommodationinformation
189	Can delete majoittujan tiedot	63	delete_accommodationinformation
190	Can add shirt size	64	add_shirtsize
191	Can change shirt size	64	change_shirtsize
192	Can delete shirt size	64	delete_shirtsize
193	Can add customer	65	add_customer
194	Can change customer	65	change_customer
195	Can delete customer	65	delete_customer
196	Can add limit group	66	add_limitgroup
197	Can change limit group	66	change_limitgroup
198	Can delete limit group	66	delete_limitgroup
199	Can add tilausrivi	67	add_orderproduct
200	Can change tilausrivi	67	change_orderproduct
201	Can delete tilausrivi	67	delete_orderproduct
202	Can add product	68	add_product
203	Can change product	68	change_product
204	Can delete product	68	delete_product
205	Can add ticket sales settings for event	69	add_ticketseventmeta
206	Can change ticket sales settings for event	69	change_ticketseventmeta
207	Can delete ticket sales settings for event	69	delete_ticketseventmeta
208	Can add shirt type	70	add_shirttype
209	Can change shirt type	70	change_shirttype
210	Can delete shirt type	70	delete_shirttype
211	Can add toimituserä	71	add_batch
212	Can change toimituserä	71	change_batch
213	Can delete toimituserä	71	delete_batch
214	Can add shirt order	72	add_shirtorder
215	Can change shirt order	72	change_shirtorder
216	Can delete shirt order	72	delete_shirtorder
217	Can add payment	73	add_payment
218	Can change payment	73	change_payment
219	Can delete payment	73	delete_payment
220	Can add tapahtuman maksunvälitystiedot	74	add_paymentseventmeta
221	Can change tapahtuman maksunvälitystiedot	74	change_paymentseventmeta
222	Can delete tapahtuman maksunvälitystiedot	74	delete_paymentseventmeta
223	Can add vastaanottajaryhmä	75	add_recipientgroup
224	Can change vastaanottajaryhmä	75	change_recipientgroup
225	Can delete vastaanottajaryhmä	75	delete_recipientgroup
226	Can add person message	76	add_personmessage
227	Can change person message	76	change_personmessage
228	Can delete person message	76	delete_personmessage
229	Can add viesti	77	add_message
230	Can change viesti	77	change_message
231	Can delete viesti	77	delete_message
232	Can add person message subject	78	add_personmessagesubject
233	Can change person message subject	78	change_personmessagesubject
234	Can delete person message subject	78	delete_personmessagesubject
235	Can add person message body	79	add_personmessagebody
236	Can change person message body	79	change_personmessagebody
237	Can delete person message body	79	delete_personmessagebody
238	Can add badge	80	add_badge
239	Can change badge	80	change_badge
240	Can delete badge	80	delete_badge
241	Can add badge management proxy	80	add_badgemanagementproxy
242	Can change badge management proxy	80	change_badgemanagementproxy
243	Can delete badge management proxy	80	delete_badgemanagementproxy
244	Can add badges event meta	81	add_badgeseventmeta
245	Can change badges event meta	81	change_badgeseventmeta
246	Can delete badges event meta	81	delete_badgeseventmeta
247	Can add Batch	82	add_batch
248	Can change Batch	82	change_batch
249	Can delete Batch	82	delete_batch
250	Can add SMTP password	84	add_smtppassword
251	Can change SMTP password	84	change_smtppassword
252	Can delete SMTP password	84	delete_smtppassword
253	Can add granted privilege	85	add_grantedprivilege
254	Can change granted privilege	85	change_grantedprivilege
255	Can delete granted privilege	85	delete_grantedprivilege
256	Can add SMTP server	86	add_smtpserver
257	Can change SMTP server	86	change_smtpserver
258	Can delete SMTP server	86	delete_smtpserver
259	Can add group privilege	87	add_groupprivilege
260	Can change group privilege	87	change_groupprivilege
261	Can delete group privilege	87	delete_groupprivilege
262	Can add access management settings	88	add_accessorganizationmeta
263	Can change access management settings	88	change_accessorganizationmeta
264	Can delete access management settings	88	delete_accessorganizationmeta
265	Can add group e-mail alias grant	89	add_groupemailaliasgrant
266	Can change group e-mail alias grant	89	change_groupemailaliasgrant
267	Can delete group e-mail alias grant	89	delete_groupemailaliasgrant
268	Can add e-mail alias type	90	add_emailaliastype
269	Can change e-mail alias type	90	change_emailaliastype
270	Can delete e-mail alias type	90	delete_emailaliastype
271	Can add Slack invite automation	91	add_slackaccess
272	Can change Slack invite automation	91	change_slackaccess
273	Can delete Slack invite automation	91	delete_slackaccess
274	Can add e-mail alias	92	add_emailalias
275	Can change e-mail alias	92	change_emailalias
276	Can delete e-mail alias	92	delete_emailalias
277	Can add e-mail alias domain	93	add_emailaliasdomain
278	Can change e-mail alias domain	93	change_emailaliasdomain
279	Can delete e-mail alias domain	93	delete_emailaliasdomain
280	Can add internal e-mail alias	94	add_internalemailalias
281	Can change internal e-mail alias	94	change_internalemailalias
282	Can delete internal e-mail alias	94	delete_internalemailalias
283	Can add privilege	95	add_privilege
284	Can change privilege	95	change_privilege
285	Can delete privilege	95	delete_privilege
286	Can add Avainsana	96	add_hotword
287	Can change Avainsana	96	change_hotword
288	Can delete Avainsana	96	delete_hotword
289	Can add Lähetetty viesti	97	add_smsmessageout
290	Can change Lähetetty viesti	97	change_smsmessageout
291	Can delete Lähetetty viesti	97	delete_smsmessageout
292	Can add Kategoria	98	add_votecategory
293	Can change Kategoria	98	change_votecategory
294	Can delete Kategoria	98	delete_votecategory
295	Can add Osallistuja	99	add_nominee
296	Can change Osallistuja	99	change_nominee
297	Can delete Osallistuja	99	delete_nominee
298	Can add Vastaanotettu viesti	100	add_smsmessagein
299	Can change Vastaanotettu viesti	100	change_smsmessagein
300	Can delete Vastaanotettu viesti	100	delete_smsmessagein
301	Can add Tekstiviestejä käyttävä tapahtuma	101	add_smseventmeta
302	Can change Tekstiviestejä käyttävä tapahtuma	101	change_smseventmeta
303	Can delete Tekstiviestejä käyttävä tapahtuma	101	delete_smseventmeta
304	Can add Ääni	102	add_vote
305	Can change Ääni	102	change_vote
306	Can delete Ääni	102	delete_vote
307	Can add Jäsenyys	103	add_membership
308	Can change Jäsenyys	103	change_membership
309	Can delete Jäsenyys	103	delete_membership
310	Can add Jäsenmaksusuoritus	104	add_membershipfeepayment
311	Can change Jäsenmaksusuoritus	104	change_membershipfeepayment
312	Can delete Jäsenmaksusuoritus	104	delete_membershipfeepayment
313	Can add Toimikausi	105	add_term
314	Can change Toimikausi	105	change_term
315	Can delete Toimikausi	105	delete_term
316	Can add Jäsenrekisterien asetukset	106	add_membershiporganizationmeta
317	Can change Jäsenrekisterien asetukset	106	change_membershiporganizationmeta
318	Can delete Jäsenrekisterien asetukset	106	delete_membershiporganizationmeta
319	Can add Team	107	add_team
320	Can change Team	107	change_team
321	Can delete Team	107	delete_team
322	Can add intra event meta	108	add_intraeventmeta
323	Can change intra event meta	108	change_intraeventmeta
324	Can delete intra event meta	108	delete_intraeventmeta
325	Can add Team member	109	add_teammember
326	Can change Team member	109	change_teammember
327	Can delete Team member	109	delete_teammember
328	Can add order	110	add_order
329	Can change order	110	change_order
330	Can delete order	110	delete_order
331	Can add code	111	add_code
332	Can change code	111	change_code
333	Can delete code	111	delete_code
334	Can add connection	112	add_connection
335	Can change connection	112	change_connection
336	Can delete connection	112	delete_connection
337	Can add confirmation code	113	add_confirmationcode
338	Can change confirmation code	113	change_confirmationcode
339	Can delete confirmation code	113	delete_confirmationcode
340	Can add special diet	114	add_specialdiet
341	Can change special diet	114	change_specialdiet
342	Can delete special diet	114	delete_specialdiet
343	Can add concon part	115	add_conconpart
344	Can change concon part	115	change_conconpart
345	Can delete concon part	115	delete_conconpart
346	Can add enrollment	116	add_enrollment
347	Can change enrollment	116	change_enrollment
348	Can delete enrollment	116	delete_enrollment
349	Can add enrollment event meta	117	add_enrollmenteventmeta
350	Can change enrollment event meta	117	change_enrollmenteventmeta
351	Can delete enrollment event meta	117	delete_enrollmenteventmeta
352	Can add feedback message	118	add_feedbackmessage
353	Can change feedback message	118	change_feedbackmessage
354	Can delete feedback message	118	delete_feedbackmessage
355	Can add log entry	119	add_entry
356	Can change log entry	119	change_entry
357	Can delete log entry	119	delete_entry
358	Can add subscription	120	add_subscription
359	Can change subscription	120	change_subscription
360	Can delete subscription	120	delete_subscription
361	Can add global survey result	121	add_globalsurveyresult
362	Can change global survey result	121	change_globalsurveyresult
363	Can delete global survey result	121	delete_globalsurveyresult
364	Can add event survey	122	add_eventsurvey
365	Can change event survey	122	change_eventsurvey
366	Can delete event survey	122	delete_eventsurvey
367	Can add event survey result	123	add_eventsurveyresult
368	Can change event survey result	123	change_eventsurveyresult
369	Can delete event survey result	123	delete_eventsurveyresult
370	Can add global survey	124	add_globalsurvey
371	Can change global survey	124	change_globalsurvey
372	Can delete global survey	124	delete_globalsurvey
373	Can add directory organization meta	125	add_directoryorganizationmeta
374	Can change directory organization meta	125	change_directoryorganizationmeta
375	Can delete directory organization meta	125	delete_directoryorganizationmeta
376	Can add directory access group	126	add_directoryaccessgroup
377	Can change directory access group	126	change_directoryaccessgroup
378	Can delete directory access group	126	delete_directoryaccessgroup
379	Can add night	127	add_night
380	Can change night	127	change_night
381	Can delete night	127	delete_night
382	Can add signup extra	128	add_signupextra
383	Can change signup extra	128	change_signupextra
384	Can delete signup extra	128	delete_signupextra
385	Can add special diet	129	add_specialdiet
386	Can change special diet	129	change_specialdiet
387	Can delete special diet	129	delete_specialdiet
388	Can add night	130	add_night
389	Can change night	130	change_night
390	Can delete night	130	delete_night
391	Can add signup extra	131	add_signupextra
392	Can change signup extra	131	change_signupextra
393	Can delete signup extra	131	delete_signupextra
394	Can add special diet	132	add_specialdiet
395	Can change special diet	132	change_specialdiet
396	Can delete special diet	132	delete_specialdiet
397	Can add special diet	133	add_specialdiet
398	Can change special diet	133	change_specialdiet
399	Can delete special diet	133	delete_specialdiet
400	Can add signup extra	134	add_signupextra
401	Can change signup extra	134	change_signupextra
402	Can delete signup extra	134	delete_signupextra
403	Can add special diet	135	add_specialdiet
404	Can change special diet	135	change_specialdiet
405	Can delete special diet	135	delete_specialdiet
406	Can add signup extra	136	add_signupextra
407	Can change signup extra	136	change_signupextra
408	Can delete signup extra	136	delete_signupextra
409	Can add signup extra	137	add_signupextra
410	Can change signup extra	137	change_signupextra
411	Can delete signup extra	137	delete_signupextra
412	Can add night	138	add_night
413	Can change night	138	change_night
414	Can delete night	138	delete_night
415	Can add special diet	139	add_specialdiet
416	Can change special diet	139	change_specialdiet
417	Can delete special diet	139	delete_specialdiet
418	Can add signup extra	140	add_signupextra
419	Can change signup extra	140	change_signupextra
420	Can delete signup extra	140	delete_signupextra
421	Can add special diet	141	add_specialdiet
422	Can change special diet	141	change_specialdiet
423	Can delete special diet	141	delete_specialdiet
424	Can add signup extra	142	add_signupextra
425	Can change signup extra	142	change_signupextra
426	Can delete signup extra	142	delete_signupextra
427	Can add special diet	143	add_specialdiet
428	Can change special diet	143	change_specialdiet
429	Can delete special diet	143	delete_specialdiet
430	Can add signup extra	144	add_signupextra
431	Can change signup extra	144	change_signupextra
432	Can delete signup extra	144	delete_signupextra
433	Can add night	145	add_night
434	Can change night	145	change_night
435	Can delete night	145	delete_night
436	Can add signup extra v2	146	add_signupextrav2
437	Can change signup extra v2	146	change_signupextrav2
438	Can delete signup extra v2	146	delete_signupextrav2
439	Can add special diet	147	add_specialdiet
440	Can change special diet	147	change_specialdiet
441	Can delete special diet	147	delete_specialdiet
442	Can add signup extra	148	add_signupextra
443	Can change signup extra	148	change_signupextra
444	Can delete signup extra	148	delete_signupextra
445	Can add special diet	149	add_specialdiet
446	Can change special diet	149	change_specialdiet
447	Can delete special diet	149	delete_specialdiet
448	Can add signup extra	150	add_signupextra
449	Can change signup extra	150	change_signupextra
450	Can delete signup extra	150	delete_signupextra
451	Can add special diet	151	add_specialdiet
452	Can change special diet	151	change_specialdiet
453	Can delete special diet	151	delete_specialdiet
454	Can add signup extra	152	add_signupextra
455	Can change signup extra	152	change_signupextra
456	Can delete signup extra	152	delete_signupextra
457	Can add signup extra	153	add_signupextra
458	Can change signup extra	153	change_signupextra
459	Can delete signup extra	153	delete_signupextra
460	Can add night	154	add_night
461	Can change night	154	change_night
462	Can delete night	154	delete_night
463	Can add special diet	155	add_specialdiet
464	Can change special diet	155	change_specialdiet
465	Can delete special diet	155	delete_specialdiet
466	Can add night	156	add_night
467	Can change night	156	change_night
468	Can delete night	156	delete_night
469	Can add special diet	157	add_specialdiet
470	Can change special diet	157	change_specialdiet
471	Can delete special diet	157	delete_specialdiet
472	Can add signup extra	158	add_signupextra
473	Can change signup extra	158	change_signupextra
474	Can delete signup extra	158	delete_signupextra
475	Can add signup extra	159	add_signupextra
476	Can change signup extra	159	change_signupextra
477	Can delete signup extra	159	delete_signupextra
478	Can add special diet	160	add_specialdiet
479	Can change special diet	160	change_specialdiet
480	Can delete special diet	160	delete_specialdiet
481	Can add signup extra v2	161	add_signupextrav2
482	Can change signup extra v2	161	change_signupextrav2
483	Can delete signup extra v2	161	delete_signupextrav2
484	Can add signup extra	162	add_signupextra
485	Can change signup extra	162	change_signupextra
486	Can delete signup extra	162	delete_signupextra
487	Can add special diet	163	add_specialdiet
488	Can change special diet	163	change_specialdiet
489	Can delete special diet	163	delete_specialdiet
490	Can add night	164	add_night
491	Can change night	164	change_night
492	Can delete night	164	delete_night
493	Can add special diet	165	add_specialdiet
494	Can change special diet	165	change_specialdiet
495	Can delete special diet	165	delete_specialdiet
496	Can add signup extra	166	add_signupextra
497	Can change signup extra	166	change_signupextra
498	Can delete signup extra	166	delete_signupextra
499	Can add special diet	167	add_specialdiet
500	Can change special diet	167	change_specialdiet
501	Can delete special diet	167	delete_specialdiet
502	Can add time slot	168	add_timeslot
503	Can change time slot	168	change_timeslot
504	Can delete time slot	168	delete_timeslot
505	Can add signup extra	169	add_signupextra
506	Can change signup extra	169	change_signupextra
507	Can delete signup extra	169	delete_signupextra
508	Can add special diet	170	add_specialdiet
509	Can change special diet	170	change_specialdiet
510	Can delete special diet	170	delete_specialdiet
511	Can add signup extra	171	add_signupextra
512	Can change signup extra	171	change_signupextra
513	Can delete signup extra	171	delete_signupextra
514	Can add signup extra	172	add_signupextra
515	Can change signup extra	172	change_signupextra
516	Can delete signup extra	172	delete_signupextra
517	Can add special diet	173	add_specialdiet
518	Can change special diet	173	change_specialdiet
519	Can delete special diet	173	delete_specialdiet
520	Can add signup extra	174	add_signupextra
521	Can change signup extra	174	change_signupextra
522	Can delete signup extra	174	delete_signupextra
523	Can add special diet	175	add_specialdiet
524	Can change special diet	175	change_specialdiet
525	Can delete special diet	175	delete_specialdiet
526	Can add event day	176	add_eventday
527	Can change event day	176	change_eventday
528	Can delete event day	176	delete_eventday
529	Can add special diet	177	add_specialdiet
530	Can change special diet	177	change_specialdiet
531	Can delete special diet	177	delete_specialdiet
532	Can add signup extra	178	add_signupextra
533	Can change signup extra	178	change_signupextra
534	Can delete signup extra	178	delete_signupextra
535	Can add signup extra	179	add_signupextra
536	Can change signup extra	179	change_signupextra
537	Can delete signup extra	179	delete_signupextra
538	Can add special diet	180	add_specialdiet
539	Can change special diet	180	change_specialdiet
540	Can delete special diet	180	delete_specialdiet
541	Can add poison	181	add_poison
542	Can change poison	181	change_poison
543	Can delete poison	181	delete_poison
544	Can add signup extra	182	add_signupextra
545	Can change signup extra	182	change_signupextra
546	Can delete signup extra	182	delete_signupextra
547	Can add night	183	add_night
548	Can change night	183	change_night
549	Can delete night	183	delete_night
550	Can add signup extra afterparty proxy	182	add_signupextraafterpartyproxy
551	Can change signup extra afterparty proxy	182	change_signupextraafterpartyproxy
552	Can delete signup extra afterparty proxy	182	delete_signupextraafterpartyproxy
553	Can add signup extra	185	add_signupextra
554	Can change signup extra	185	change_signupextra
555	Can delete signup extra	185	delete_signupextra
556	Can add special diet	186	add_specialdiet
557	Can change special diet	186	change_specialdiet
558	Can delete special diet	186	delete_specialdiet
559	Can add signup extra	187	add_signupextra
560	Can change signup extra	187	change_signupextra
561	Can delete signup extra	187	delete_signupextra
562	Can add special diet	188	add_specialdiet
563	Can change special diet	188	change_specialdiet
564	Can delete special diet	188	delete_specialdiet
565	Can add signup extra	189	add_signupextra
566	Can change signup extra	189	change_signupextra
567	Can delete signup extra	189	delete_signupextra
568	Can add night	190	add_night
569	Can change night	190	change_night
570	Can delete night	190	delete_night
571	Can add shift	191	add_shift
572	Can change shift	191	change_shift
573	Can delete shift	191	delete_shift
574	Can add signup extra	192	add_signupextra
575	Can change signup extra	192	change_signupextra
576	Can delete signup extra	192	delete_signupextra
577	Can add signup extra	193	add_signupextra
578	Can change signup extra	193	change_signupextra
579	Can delete signup extra	193	delete_signupextra
580	Can add special diet	194	add_specialdiet
581	Can change special diet	194	change_specialdiet
582	Can delete special diet	194	delete_specialdiet
583	Can add signup extra	195	add_signupextra
584	Can change signup extra	195	change_signupextra
585	Can delete signup extra	195	delete_signupextra
586	Can add event day	196	add_eventday
587	Can change event day	196	change_eventday
588	Can delete event day	196	delete_eventday
589	Can add special diet	197	add_specialdiet
590	Can change special diet	197	change_specialdiet
591	Can delete special diet	197	delete_specialdiet
592	Can add signup extra	198	add_signupextra
593	Can change signup extra	198	change_signupextra
594	Can delete signup extra	198	delete_signupextra
595	Can add signup extra	199	add_signupextra
596	Can change signup extra	199	change_signupextra
597	Can delete signup extra	199	delete_signupextra
598	Can add special diet	200	add_specialdiet
599	Can change special diet	200	change_specialdiet
600	Can delete special diet	200	delete_specialdiet
601	Can add signup extra	201	add_signupextra
602	Can change signup extra	201	change_signupextra
603	Can delete signup extra	201	delete_signupextra
604	Can add night	202	add_night
605	Can change night	202	change_night
606	Can delete night	202	delete_night
607	Can add view room	203	add_viewroom
608	Can change view room	203	change_viewroom
609	Can delete view room	203	delete_viewroom
610	Can add listing	204	add_listing
611	Can change listing	204	change_listing
612	Can delete listing	204	delete_listing
613	Can add external event	205	add_externalevent
614	Can change external event	205	change_externalevent
615	Can delete external event	205	delete_externalevent
616	Can add signup extra afterparty proxy	201	add_signupextraafterpartyproxy
617	Can change signup extra afterparty proxy	201	change_signupextraafterpartyproxy
618	Can delete signup extra afterparty proxy	201	delete_signupextraafterpartyproxy
619	Can add poison	206	add_poison
620	Can change poison	206	change_poison
621	Can delete poison	206	delete_poison
622	Can add signup extra	208	add_signupextra
623	Can change signup extra	208	change_signupextra
624	Can delete signup extra	208	delete_signupextra
625	Can add special diet	209	add_specialdiet
626	Can change special diet	209	change_specialdiet
627	Can delete special diet	209	delete_specialdiet
628	Can add signup extra	210	add_signupextra
629	Can change signup extra	210	change_signupextra
630	Can delete signup extra	210	delete_signupextra
631	Can add special diet	211	add_specialdiet
632	Can change special diet	211	change_specialdiet
633	Can delete special diet	211	delete_specialdiet
634	Can add signup extra	212	add_signupextra
635	Can change signup extra	212	change_signupextra
636	Can delete signup extra	212	delete_signupextra
637	Can add signup extra	213	add_signupextra
638	Can change signup extra	213	change_signupextra
639	Can delete signup extra	213	delete_signupextra
640	Can add time slot	214	add_timeslot
641	Can change time slot	214	change_timeslot
642	Can delete time slot	214	delete_timeslot
643	Can add special diet	215	add_specialdiet
644	Can change special diet	215	change_specialdiet
645	Can delete special diet	215	delete_specialdiet
646	Can add signup extra	216	add_signupextra
647	Can change signup extra	216	change_signupextra
648	Can delete signup extra	216	delete_signupextra
649	Can add special diet	217	add_specialdiet
650	Can change special diet	217	change_specialdiet
651	Can delete special diet	217	delete_specialdiet
652	Can add signup extra	218	add_signupextra
653	Can change signup extra	218	change_signupextra
654	Can delete signup extra	218	delete_signupextra
655	Can add night	219	add_night
656	Can change night	219	change_night
657	Can delete night	219	delete_night
658	Can add special diet	220	add_specialdiet
659	Can change special diet	220	change_specialdiet
660	Can delete special diet	220	delete_specialdiet
661	Can add signup extra	221	add_signupextra
662	Can change signup extra	221	change_signupextra
663	Can delete signup extra	221	delete_signupextra
664	Can add special diet	222	add_specialdiet
665	Can change special diet	222	change_specialdiet
666	Can delete special diet	222	delete_specialdiet
667	Can add signup extra	223	add_signupextra
668	Can change signup extra	223	change_signupextra
669	Can delete signup extra	223	delete_signupextra
670	Can add event day	224	add_eventday
671	Can change event day	224	change_eventday
672	Can delete event day	224	delete_eventday
673	Can add special diet	225	add_specialdiet
674	Can change special diet	225	change_specialdiet
675	Can delete special diet	225	delete_specialdiet
676	Can add signup extra	226	add_signupextra
677	Can change signup extra	226	change_signupextra
678	Can delete signup extra	226	delete_signupextra
679	Can add special diet	227	add_specialdiet
680	Can change special diet	227	change_specialdiet
681	Can delete special diet	227	delete_specialdiet
682	Can add signup extra	228	add_signupextra
683	Can change signup extra	228	change_signupextra
684	Can delete signup extra	228	delete_signupextra
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: badges_badge; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.badges_badge (id, printed_separately_at, revoked_at, job_title, created_at, updated_at, batch_id, person_id, personnel_class_id, first_name, is_first_name_visible, is_nick_visible, is_surname_visible, nick, surname, created_by_id, revoked_by_id, arrived_at, notes) FROM stdin;
\.


--
-- Data for Name: badges_badgeseventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.badges_badgeseventmeta (event_id, admin_group_id, badge_layout, real_name_must_be_visible, is_using_fuzzy_reissuance_hack) FROM stdin;
\.


--
-- Data for Name: badges_batch; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.badges_batch (id, created_at, updated_at, printed_at, event_id, personnel_class_id) FROM stdin;
\.


--
-- Data for Name: core_carouselslide; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_carouselslide (id, active_from, active_until, href, title, image_file, image_credit, target, "order") FROM stdin;
\.


--
-- Data for Name: core_emailverificationtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_emailverificationtoken (id, code, created_at, used_at, state, email, person_id) FROM stdin;
\.


--
-- Data for Name: core_event; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_event (id, slug, name, name_genitive, name_illative, name_inessive, description, start_time, end_time, homepage_url, public, venue_id, logo_url, organization_id, panel_css_class, logo_file) FROM stdin;
\.


--
-- Data for Name: core_organization; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_organization (id, slug, name, homepage_url, description, logo_url, public, muncipality, name_genitive) FROM stdin;
\.


--
-- Data for Name: core_passwordresettoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_passwordresettoken (id, code, created_at, used_at, state, ip_address, person_id) FROM stdin;
\.


--
-- Data for Name: core_person; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_person (id, first_name, surname, nick, birth_date, email, phone, may_send_info, preferred_name_display_style, notes, email_verified_at, user_id, muncipality, official_first_names, allow_work_history_sharing) FROM stdin;
\.


--
-- Data for Name: core_venue; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.core_venue (id, name, name_inessive) FROM stdin;
\.


--
-- Data for Name: desucon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2016_signupextra (signup_id, shift_type, desu_amount, prior_experience, free_text, shirt_size, shirt_type, night_work, special_diet_other, is_active) FROM stdin;
\.


--
-- Data for Name: desucon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: desucon2016_signupextrav2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2016_signupextrav2 (id, shift_type, desu_amount, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, event_id, person_id, is_active) FROM stdin;
\.


--
-- Data for Name: desucon2016_signupextrav2_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2016_signupextrav2_special_diet (id, signupextrav2_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: desucon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: desucon2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2017_signupextra (id, is_active, shift_type, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: desucon2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: desucon2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: desucon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2018_signupextra (id, is_active, shift_type, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, event_id, person_id, afterparty_participation) FROM stdin;
\.


--
-- Data for Name: desucon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: desucon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: desucon2019_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2019_signupextra (id, is_active, shift_type, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, afterparty_participation, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: desucon2019_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2019_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: desucon2019_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desucon2019_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: desuprofile_integration_confirmationcode; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desuprofile_integration_confirmationcode (id, code, created_at, used_at, state, desuprofile_id, person_id, next_url, desuprofile_username) FROM stdin;
\.


--
-- Data for Name: desuprofile_integration_connection; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.desuprofile_integration_connection (id, user_id, desuprofile_username) FROM stdin;
\.


--
-- Data for Name: directory_directoryaccessgroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.directory_directoryaccessgroup (id, active_from, active_until, created_at, updated_at, group_id, organization_id) FROM stdin;
\.


--
-- Data for Name: directory_directoryorganizationmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.directory_directoryorganizationmeta (organization_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	user
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	sites	site
7	admin	logentry
8	oauth2_provider	refreshtoken
9	oauth2_provider	accesstoken
10	oauth2_provider	grant
11	oauth2_provider	application
12	nexmo	inboundmessagefragment
13	nexmo	inboundmessage
14	nexmo	deliverystatusfragment
15	nexmo	outboundmessage
16	core	carouselslide
17	core	person
18	core	organization
19	core	venue
20	core	passwordresettoken
21	core	emailverificationtoken
22	core	event
23	programme	specialstarttime
24	programme	category
25	programme	role
26	programme	tag
27	programme	freeformorganizer
28	programme	invitation
29	programme	programmefeedback
30	programme	alternativeprogrammeform
31	programme	view
32	programme	programmeeventmeta
33	programme	timeblock
34	programme	programmerole
35	programme	programme
36	programme	room
37	programme	invitationadminproxy
38	programme	coldoffersprogrammeeventmetaproxy
39	programme	programmemanagementproxy
40	programme	freeformorganizeradminproxy
41	labour	signup
42	labour	perk
43	labour	obsoleteemptysignupextrav1
44	labour	jobrequirement
45	labour	shift
46	labour	qualification
47	labour	alternativesignupform
48	labour	jobcategory
49	labour	job
50	labour	infolink
51	labour	personqualification
52	labour	survey
53	labour	surveyrecord
54	labour	workperiod
55	labour	laboureventmeta
56	labour	emptysignupextra
57	labour	personnelclass
58	labour	signupcertificateproxy
59	labour	jobcategorymanagementproxy
60	labour	signuponboardingproxy
61	labour_common_qualifications	jvkortti
62	tickets	order
63	tickets	accommodationinformation
64	tickets	shirtsize
65	tickets	customer
66	tickets	limitgroup
67	tickets	orderproduct
68	tickets	product
69	tickets	ticketseventmeta
70	tickets	shirttype
71	tickets	batch
72	tickets	shirtorder
73	payments	payment
74	payments	paymentseventmeta
75	mailings	recipientgroup
76	mailings	personmessage
77	mailings	message
78	mailings	personmessagesubject
79	mailings	personmessagebody
80	badges	badge
81	badges	badgeseventmeta
82	badges	batch
83	badges	badgemanagementproxy
84	access	smtppassword
85	access	grantedprivilege
86	access	smtpserver
87	access	groupprivilege
88	access	accessorganizationmeta
89	access	groupemailaliasgrant
90	access	emailaliastype
91	access	slackaccess
92	access	emailalias
93	access	emailaliasdomain
94	access	internalemailalias
95	access	privilege
96	sms	hotword
97	sms	smsmessageout
98	sms	votecategory
99	sms	nominee
100	sms	smsmessagein
101	sms	smseventmeta
102	sms	vote
103	membership	membership
104	membership	membershipfeepayment
105	membership	term
106	membership	membershiporganizationmeta
107	intra	team
108	intra	intraeventmeta
109	intra	teammember
110	lippukala	order
111	lippukala	code
112	desuprofile_integration	connection
113	desuprofile_integration	confirmationcode
114	enrollment	specialdiet
115	enrollment	conconpart
116	enrollment	enrollment
117	enrollment	enrollmenteventmeta
118	feedback	feedbackmessage
119	event_log	entry
120	event_log	subscription
121	surveys	globalsurveyresult
122	surveys	eventsurvey
123	surveys	eventsurveyresult
124	surveys	globalsurvey
125	directory	directoryorganizationmeta
126	directory	directoryaccessgroup
127	tracon9	night
128	tracon9	signupextra
129	tracon9	specialdiet
130	traconx	night
131	traconx	signupextra
132	traconx	specialdiet
133	hitpoint2015	specialdiet
134	hitpoint2015	signupextra
135	kuplii2015	specialdiet
136	kuplii2015	signupextra
137	animecon2015	signupextra
138	animecon2015	night
139	animecon2015	specialdiet
140	yukicon2016	signupextra
141	yukicon2016	specialdiet
142	finncon2016	signupextra
143	finncon2016	specialdiet
144	frostbite2016	signupextra
145	tracon11	night
146	tracon11	signupextrav2
147	tracon11	specialdiet
148	tracon11	signupextra
149	kuplii2016	specialdiet
150	kuplii2016	signupextra
151	aicon2016	specialdiet
152	aicon2016	signupextra
153	kawacon2016	signupextra
154	kawacon2016	night
155	kawacon2016	specialdiet
156	mimicon2016	night
157	mimicon2016	specialdiet
158	mimicon2016	signupextra
159	desucon2016	signupextra
160	desucon2016	specialdiet
161	desucon2016	signupextrav2
162	lakeuscon2016	signupextra
163	lakeuscon2016	specialdiet
164	animecon2016	night
165	animecon2016	specialdiet
166	animecon2016	signupextra
167	hitpoint2017	specialdiet
168	hitpoint2017	timeslot
169	hitpoint2017	signupextra
170	tylycon2017	specialdiet
171	tylycon2017	signupextra
172	shippocon2016	signupextra
173	shippocon2016	specialdiet
174	yukicon2017	signupextra
175	yukicon2017	specialdiet
176	yukicon2017	eventday
177	frostbite2017	specialdiet
178	frostbite2017	signupextra
179	kuplii2017	signupextra
180	kuplii2017	specialdiet
181	tracon2017	poison
182	tracon2017	signupextra
183	tracon2017	night
184	tracon2017	signupextraafterpartyproxy
185	popcult2017	signupextra
186	desucon2017	specialdiet
187	desucon2017	signupextra
188	kawacon2017	specialdiet
189	kawacon2017	signupextra
190	kawacon2017	night
191	kawacon2017	shift
192	worldcon75	signupextra
193	frostbite2018	signupextra
194	frostbite2018	specialdiet
195	yukicon2018	signupextra
196	yukicon2018	eventday
197	yukicon2018	specialdiet
198	nippori2017	signupextra
199	kuplii2018	signupextra
200	kuplii2018	specialdiet
201	tracon2018	signupextra
202	tracon2018	night
203	programme	viewroom
204	listings	listing
205	listings	externalevent
206	tracon2018	poison
207	tracon2018	signupextraafterpartyproxy
208	aicon2018	signupextra
209	aicon2018	specialdiet
210	popcultday2018	signupextra
211	desucon2018	specialdiet
212	desucon2018	signupextra
213	matsucon2018	signupextra
214	ropecon2018	timeslot
215	ropecon2018	specialdiet
216	ropecon2018	signupextra
217	finncon2018	specialdiet
218	finncon2018	signupextra
219	mimicon2018	night
220	mimicon2018	specialdiet
221	mimicon2018	signupextra
222	yukicon2019	specialdiet
223	yukicon2019	signupextra
224	yukicon2019	eventday
225	frostbite2019	specialdiet
226	frostbite2019	signupextra
227	desucon2019	specialdiet
228	desucon2019	signupextra
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2017-11-13 20:04:45.024226+00
2	auth	0001_initial	2017-11-13 20:04:45.141516+00
3	core	0001_initial	2017-11-13 20:04:45.287537+00
4	core	0002_auto_20150126_1611	2017-11-13 20:04:45.308859+00
5	core	0003_auto_20150813_1907	2017-11-13 20:04:45.323461+00
6	core	0004_organization	2017-11-13 20:04:45.365789+00
7	core	0005_auto_20151008_2225	2017-11-13 20:04:45.434296+00
8	core	0006_organization_description	2017-11-13 20:04:45.468413+00
9	core	0007_organization_logo_url	2017-11-13 20:04:45.504799+00
10	core	0008_person_muncipality	2017-11-13 20:04:45.54563+00
11	core	0009_auto_20151010_1632	2017-11-13 20:04:45.566835+00
12	core	0010_organization_public	2017-11-13 20:04:45.598564+00
13	core	0011_organization_muncipality	2017-11-13 20:04:45.628194+00
14	core	0012_auto_20151011_1926	2017-11-13 20:04:45.701317+00
15	core	0013_auto_20151011_2005	2017-11-13 20:04:45.753637+00
16	core	0014_auto_20151011_2016	2017-11-13 20:04:45.774689+00
17	core	0015_organization_name_genitive	2017-11-13 20:04:45.802974+00
18	core	0016_person_allow_work_history_sharing	2017-11-13 20:04:45.837111+00
19	core	0017_remove_event_headline	2017-11-13 20:04:45.861985+00
20	core	0018_auto_20160124_1447	2017-11-13 20:04:45.905487+00
21	core	0019_auto_20160129_2140	2017-11-13 20:04:45.98355+00
22	core	0020_auto_20160131_2044	2017-11-13 20:04:46.011625+00
23	core	0021_auto_20160202_1950	2017-11-13 20:04:46.038832+00
24	core	0022_auto_20160202_2235	2017-11-13 20:04:46.06487+00
25	access	0001_initial	2017-11-13 20:04:46.25548+00
26	access	0002_grantedprivilege_state	2017-11-13 20:04:46.290713+00
27	access	0003_slackaccess	2017-11-13 20:04:46.330794+00
28	access	0004_descriptions	2017-11-13 20:04:46.437108+00
29	access	0005_email_aliases	2017-11-13 20:04:46.808342+00
30	access	0006_group_grant_active_until	2017-11-13 20:04:46.902365+00
31	access	0007_accessorganizationmeta	2017-11-13 20:04:46.96554+00
32	access	0008_smtp	2017-11-13 20:04:47.122483+00
33	access	0009_privilege_disclaimers	2017-11-13 20:04:47.174552+00
34	access	0010_auto_20151106_1500	2017-11-13 20:04:47.289095+00
35	access	0011_auto_20160202_2235	2017-11-13 20:04:47.343125+00
36	access	0012_auto_20160607_2224	2017-11-13 20:04:48.506735+00
37	access	0013_auto_20160608_0018	2017-11-13 20:04:48.641889+00
38	access	0014_emailaliastype_priority	2017-11-13 20:04:48.813195+00
39	access	0015_auto_20170416_2044	2017-11-13 20:04:48.856359+00
40	admin	0001_initial	2017-11-13 20:04:48.93074+00
41	admin	0002_logentry_remove_auto_add	2017-11-13 20:04:48.971617+00
42	labour	0001_initial	2017-11-13 20:04:50.43599+00
43	labour	0002_auto_20141115_1102	2017-11-13 20:04:50.819418+00
44	badges	0001_initial	2017-11-13 20:04:51.43515+00
45	labour	0003_populate_pclasses	2017-11-13 20:04:51.444738+00
46	labour	0004_auto_20141115_1337	2017-11-13 20:04:51.546776+00
47	labour	0005_jobcategory_app_label	2017-11-13 20:04:51.629278+00
48	labour	0006_auto_20141115_1348	2017-11-13 20:04:51.758898+00
49	labour	0007_jobcategory_personnel_classes	2017-11-13 20:04:51.851891+00
50	labour	0008_auto_20150419_1438	2017-11-13 20:04:51.980577+00
51	labour	0009_remove_signup_work_periods	2017-11-13 20:04:52.172112+00
52	labour	0010_auto_20150929_1545	2017-11-13 20:04:52.262819+00
53	labour	0011_job_slug	2017-11-13 20:04:52.413478+00
54	labour	0012_auto_20151017_0012	2017-11-13 20:04:52.533339+00
55	labour	0013_signup_time_confirmation_requested	2017-11-13 20:04:52.621179+00
56	aicon2016	0001_initial	2017-11-13 20:04:52.807181+00
57	aicon2016	0002_signupextra_email_alias	2017-11-13 20:04:52.87978+00
58	aicon2016	0003_auto_20160306_1125	2017-11-13 20:04:52.995929+00
59	aicon2016	0004_signupextra_is_active	2017-11-13 20:04:53.077916+00
60	aicon2016	0005_auto_20170416_2044	2017-11-13 20:04:53.31746+00
61	animecon2015	0001_initial	2017-11-13 20:04:53.529555+00
62	animecon2015	0002_remove_signupextra_construction	2017-11-13 20:04:53.618627+00
63	animecon2015	0003_auto_20150303_2332	2017-11-13 20:04:53.705467+00
64	animecon2015	0004_signupextra_personal_identification_number	2017-11-13 20:04:53.820951+00
65	animecon2015	0005_remove_signupextra_shirt_size	2017-11-13 20:04:53.901064+00
66	animecon2015	0006_auto_20150309_2309	2017-11-13 20:04:54.036314+00
67	animecon2015	0007_auto_20150309_2312	2017-11-13 20:04:54.295395+00
68	animecon2015	0008_auto_20150419_1438	2017-11-13 20:04:54.365486+00
69	animecon2015	0009_auto_20160306_1125	2017-11-13 20:04:54.500294+00
70	animecon2015	0010_signupextra_is_active	2017-11-13 20:04:54.5899+00
71	labour	0014_auto_20151108_1906	2017-11-13 20:04:54.709079+00
72	labour	0015_auto_20160124_2328	2017-11-13 20:04:55.64969+00
73	labour	0016_auto_20160128_1805	2017-11-13 20:04:55.792054+00
74	labour	0017_auto_20160201_0050	2017-11-13 20:04:55.905005+00
75	labour	0018_auto_20160202_2235	2017-11-13 20:04:56.43974+00
76	labour	0019_auto_20160207_2330	2017-11-13 20:04:57.172286+00
77	labour	0020_signup_job_categories_rejected	2017-11-13 20:04:57.274194+00
78	labour	0021_auto_20160306_1125	2017-11-13 20:04:57.375888+00
79	animecon2016	0001_initial	2017-11-13 20:04:57.575666+00
80	animecon2016	0002_signupextra_is_active	2017-11-13 20:04:57.644301+00
81	contenttypes	0002_remove_content_type_name	2017-11-13 20:04:57.987305+00
82	auth	0002_alter_permission_name_max_length	2017-11-13 20:04:58.125235+00
83	auth	0003_alter_user_email_max_length	2017-11-13 20:04:58.308023+00
84	auth	0004_alter_user_username_opts	2017-11-13 20:04:58.39724+00
85	auth	0005_alter_user_last_login_null	2017-11-13 20:04:58.492454+00
86	auth	0006_require_contenttypes_0002	2017-11-13 20:04:58.496827+00
87	auth	0007_alter_validators_add_error_messages	2017-11-13 20:04:58.589147+00
88	auth	0008_alter_user_username_max_length	2017-11-13 20:04:58.767289+00
89	badges	0002_personnel_class	2017-11-13 20:04:58.92863+00
90	badges	0003_populate_personnel_class	2017-11-13 20:04:58.938744+00
91	badges	0004_remove_template	2017-11-13 20:04:59.132416+00
92	badges	0005_badge_layout	2017-11-13 20:04:59.361921+00
93	badges	0006_badgeseventmeta_real_name_must_be_visible	2017-11-13 20:04:59.449869+00
94	badges	0007_remove_badgeseventmeta_badge_factory_code	2017-11-13 20:04:59.656504+00
95	badges	0008_auto_20160129_1838	2017-11-13 20:05:00.536215+00
96	badges	0009_add_denormalized_fields	2017-11-13 20:05:00.958179+00
97	badges	0010_populate_denormalized_fields	2017-11-13 20:05:00.967476+00
98	badges	0011_make_denormalized_fields_mandatory	2017-11-13 20:05:01.288769+00
99	badges	0012_delete_spurious_badges	2017-11-13 20:05:01.298656+00
100	badges	0013_make_personnel_class_mandatory	2017-11-13 20:05:01.393266+00
101	badges	0014_auto_20160129_2230	2017-11-13 20:05:01.54708+00
102	badges	0015_auto_20160129_2245	2017-11-13 20:05:01.955818+00
103	badges	0016_auto_20160129_2339	2017-11-13 20:05:02.042101+00
104	badges	0017_badgemanagementproxy	2017-11-13 20:05:02.054719+00
105	badges	0018_badge_arrived_at	2017-11-13 20:05:02.179772+00
106	badges	0019_auto_20160627_2018	2017-11-13 20:05:02.359197+00
107	badges	0020_auto_20160706_2207	2017-11-13 20:05:02.436865+00
108	badges	0021_auto_20170830_2237	2017-11-13 20:05:02.898352+00
109	badges	0022_badge_notes	2017-11-13 20:05:02.993157+00
110	core	0023_auto_20160704_2155	2017-11-13 20:05:03.087942+00
111	core	0024_carouselslide	2017-11-13 20:05:03.11098+00
112	core	0025_auto_20170722_1954	2017-11-13 20:05:03.137839+00
113	core	0026_auto_20170722_1958	2017-11-13 20:05:03.151454+00
114	core	0027_event_panel_css_class	2017-11-13 20:05:03.282017+00
115	core	0028_auto_20170802_1453	2017-11-13 20:05:03.381585+00
116	core	0029_auto_20170827_1818	2017-11-13 20:05:03.482179+00
117	desucon2016	0001_initial	2017-11-13 20:05:03.591938+00
118	desucon2016	0002_auto_20160128_2321	2017-11-13 20:05:03.788549+00
119	desucon2016	0003_auto_20160128_2327	2017-11-13 20:05:04.053386+00
120	desucon2016	0004_auto_20160129_0148	2017-11-13 20:05:04.143328+00
121	desucon2016	0005_auto_20160306_1125	2017-11-13 20:05:04.264692+00
122	desucon2016	0006_signupextrav2	2017-11-13 20:05:04.389935+00
123	desucon2016	0007_migrate_to_signupextrav2	2017-11-13 20:05:04.400088+00
124	desucon2016	0008_auto_20160406_2151	2017-11-13 20:05:04.593484+00
125	desucon2016	0009_auto_20160505_2233	2017-11-13 20:05:04.857657+00
126	desucon2017	0001_initial	2017-11-13 20:05:05.056707+00
127	desucon2017	0002_remove_signupextra_desu_amount	2017-11-13 20:05:05.147594+00
128	desucon2017	0003_auto_20170522_2313	2017-11-13 20:05:05.342856+00
129	desuprofile_integration	0001_initial	2017-11-13 20:05:05.726503+00
130	desuprofile_integration	0002_confirmationcode_next_url	2017-11-13 20:05:05.843893+00
131	desuprofile_integration	0003_auto_20151016_2135	2017-11-13 20:05:06.035699+00
132	desuprofile_integration	0004_auto_20151108_1905	2017-11-13 20:05:06.1408+00
133	desuprofile_integration	0005_auto_20160124_2328	2017-11-13 20:05:06.231869+00
134	directory	0001_initial	2017-11-13 20:05:06.60079+00
135	enrollment	0001_initial	2017-11-13 20:05:07.024077+00
136	enrollment	0002_enrollmenteventmeta_override_enrollment_form_message	2017-11-13 20:05:07.130432+00
137	enrollment	0003_auto_20170417_2259	2017-11-13 20:05:07.372736+00
138	enrollment	0004_auto_20170926_1851	2017-11-13 20:05:08.120502+00
139	enrollment	0005_auto_20170928_1334	2017-11-13 20:05:08.46345+00
140	surveys	0001_initial	2017-11-13 20:05:09.099651+00
141	surveys	0002_auto_20170321_2103	2017-11-13 20:05:09.311596+00
142	feedback	0001_initial	2017-11-13 20:05:09.44064+00
143	event_log	0001_initial	2017-11-13 20:05:09.753336+00
144	event_log	0002_auto_20170416_2048	2017-11-13 20:05:10.540134+00
145	event_log	0003_subscription_event_survey_filter	2017-11-13 20:05:10.792399+00
146	event_log	0004_entry_context	2017-11-13 20:05:10.940143+00
147	event_log	0005_entry_person	2017-11-13 20:05:11.112506+00
148	event_log	0006_auto_20170915_1845	2017-11-13 20:05:11.388577+00
149	event_log	0007_entry_ip_address	2017-11-13 20:05:11.537704+00
150	finncon2016	0001_initial	2017-11-13 20:05:11.947302+00
151	finncon2016	0002_auto_20160127_1806	2017-11-13 20:05:12.211141+00
152	finncon2016	0003_auto_20160127_1812	2017-11-13 20:05:12.321316+00
153	finncon2016	0004_auto_20160306_1125	2017-11-13 20:05:12.467219+00
154	finncon2016	0005_signupextra_is_active	2017-11-13 20:05:12.702247+00
155	frostbite2016	0001_initial	2017-11-13 20:05:12.844222+00
156	frostbite2016	0002_desu_amount_must_be_natural	2017-11-13 20:05:12.978268+00
157	frostbite2016	0003_auto_20151108_2350	2017-11-13 20:05:13.102542+00
158	frostbite2016	0004_auto_20151109_2316	2017-11-13 20:05:13.334602+00
159	frostbite2016	0005_auto_20160306_1125	2017-11-13 20:05:13.569226+00
160	frostbite2016	0006_signupextra_is_active	2017-11-13 20:05:13.693495+00
161	frostbite2017	0001_initial	2017-11-13 20:05:14.003448+00
162	frostbite2017	0002_auto_20170131_2323	2017-11-13 20:05:14.264561+00
163	frostbite2018	0001_initial	2017-11-13 20:05:14.663189+00
164	hitpoint2015	0001_initial	2017-11-13 20:05:14.984005+00
165	hitpoint2015	0002_auto_20150930_2244	2017-11-13 20:05:15.787915+00
166	hitpoint2015	0003_auto_20150930_2248	2017-11-13 20:05:15.934875+00
167	hitpoint2015	0004_auto_20150930_2252	2017-11-13 20:05:16.391266+00
168	hitpoint2015	0005_remove_signupextra_shirt_size	2017-11-13 20:05:16.521276+00
169	hitpoint2015	0006_auto_20151005_2348	2017-11-13 20:05:16.64211+00
170	hitpoint2015	0007_auto_20160306_1125	2017-11-13 20:05:16.808569+00
171	hitpoint2015	0008_signupextra_is_active	2017-11-13 20:05:17.092813+00
172	hitpoint2015	0009_auto_20170416_2044	2017-11-13 20:05:17.347304+00
173	hitpoint2017	0001_initial	2017-11-13 20:05:17.623305+00
174	hitpoint2017	0002_signupextra_is_active	2017-11-13 20:05:17.765673+00
175	hitpoint2017	0003_timeslot	2017-11-13 20:05:17.779372+00
176	hitpoint2017	0004_auto_20170122_1920	2017-11-13 20:05:18.073133+00
177	intra	0001_initial	2017-11-13 20:05:18.900825+00
178	intra	0002_auto_20161020_2143	2017-11-13 20:05:19.065565+00
179	intra	0003_team_email	2017-11-13 20:05:19.237777+00
180	intra	0004_teammember_override_name_display_style	2017-11-13 20:05:19.394935+00
181	intra	0005_teammember_override_job_title	2017-11-13 20:05:19.553363+00
182	intra	0006_auto_20171113_2158	2017-11-13 20:05:20.200749+00
183	kawacon2016	0001_initial	2017-11-13 20:05:20.5805+00
184	kawacon2016	0002_auto_20160127_1922	2017-11-13 20:05:20.838997+00
185	kawacon2016	0003_auto_20160127_1924	2017-11-13 20:05:21.017307+00
186	kawacon2016	0004_auto_20160306_1125	2017-11-13 20:05:21.166934+00
187	kawacon2016	0005_signupextra_is_active	2017-11-13 20:05:21.418172+00
188	kawacon2017	0001_initial	2017-11-13 20:05:21.728775+00
189	kawacon2017	0002_signupextra_want_certificate	2017-11-13 20:05:21.8794+00
190	kawacon2017	0003_auto_20170316_0030	2017-11-13 20:05:22.05309+00
191	kuplii2015	0001_initial	2017-11-13 20:05:22.458764+00
192	kuplii2015	0002_remove_signupextra_construction	2017-11-13 20:05:22.616426+00
193	kuplii2015	0003_auto_20160306_1125	2017-11-13 20:05:22.779372+00
194	kuplii2015	0004_signupextra_is_active	2017-11-13 20:05:23.044891+00
195	kuplii2016	0001_initial	2017-11-13 20:05:23.344124+00
196	kuplii2016	0002_auto_20160306_1125	2017-11-13 20:05:23.506799+00
197	kuplii2016	0003_signupextra_is_active	2017-11-13 20:05:23.659614+00
198	kuplii2017	0001_initial	2017-11-13 20:05:24.102002+00
199	kuplii2018	0001_initial	2017-11-13 20:05:24.420475+00
200	labour	0022_rename_empty_signup_extra	2017-11-13 20:05:24.687273+00
201	labour	0023_auto_20160406_1828	2017-11-13 20:05:24.843358+00
202	labour	0024_emptysignupextra	2017-11-13 20:05:25.010424+00
203	labour	0025_auto_20160406_2144	2017-11-13 20:05:25.371221+00
204	labour	0015_shift	2017-11-13 20:05:25.531324+00
205	labour	0016_auto_20151205_1321	2017-11-13 20:05:25.670661+00
206	labour	0026_merge	2017-11-13 20:05:25.679824+00
207	labour	0027_auto_20160505_2233	2017-11-13 20:05:27.905852+00
208	labour	0028_auto_20160608_0018	2017-11-13 20:05:28.059519+00
209	labour	0029_auto_20160608_2309	2017-11-13 20:05:28.346447+00
210	labour	0030_auto_20160716_1419	2017-11-13 20:05:28.990342+00
211	labour	0031_surveyrecord	2017-11-13 20:05:29.160794+00
212	labour	0032_survey_override_does_not_apply_message	2017-11-13 20:05:29.339588+00
213	labour	0033_auto_20170802_1500	2017-11-13 20:05:29.766252+00
214	labour_common_qualifications	0001_initial	2017-11-13 20:05:29.929273+00
215	labour_common_qualifications	0002_auto_20150521_1557	2017-11-13 20:05:30.091258+00
216	labour_common_qualifications	0003_auto_20151220_1552	2017-11-13 20:05:30.254312+00
217	lakeuscon2016	0001_initial	2017-11-13 20:05:30.721368+00
218	lakeuscon2016	0002_auto_20160221_2245	2017-11-13 20:05:30.883425+00
219	lakeuscon2016	0003_auto_20160306_1125	2017-11-13 20:05:31.089378+00
220	lakeuscon2016	0004_signupextra_is_active	2017-11-13 20:05:31.396654+00
221	lakeuscon2016	0005_auto_20170416_2044	2017-11-13 20:05:31.594566+00
222	lippukala	0001_initial	2017-11-13 20:05:31.660772+00
223	lippukala	0002_soft_prefixes	2017-11-13 20:05:31.686193+00
224	mailings	0001_initial	2017-11-13 20:05:32.545328+00
225	mailings	0002_message_channel	2017-11-13 20:05:32.743263+00
226	mailings	0003_message_channel_help	2017-11-13 20:05:32.912418+00
227	mailings	0004_recipientgroup_job_category	2017-11-13 20:05:33.246619+00
228	mailings	0005_populate_recipient_group_job_category	2017-11-13 20:05:33.257509+00
229	mailings	0006_auto_20160505_2233	2017-11-13 20:05:33.446616+00
230	mailings	0007_recipientgroup_personnel_class	2017-11-13 20:05:33.632448+00
231	mailings	0008_auto_20161026_2343	2017-11-13 20:05:34.196136+00
232	membership	0001_initial	2017-11-13 20:05:34.775056+00
233	membership	0002_membershiporganizationmeta_receiving_applications	2017-11-13 20:05:34.932384+00
234	membership	0003_requirements	2017-11-13 20:05:35.338127+00
235	membership	0004_auto_20151010_1632	2017-11-13 20:05:35.760825+00
236	membership	0005_membership_message	2017-11-13 20:05:36.049423+00
237	membership	0006_auto_20151011_2005	2017-11-13 20:05:36.767954+00
238	membership	0007_auto_20151011_2109	2017-11-13 20:05:36.927875+00
239	membership	0008_auto_20151011_2229	2017-11-13 20:05:37.6622+00
240	membership	0009_auto_20151011_2236	2017-11-13 20:05:37.827818+00
241	membership	0010_remove_membershiporganizationmeta_membership_fee	2017-11-13 20:05:37.999264+00
242	membership	0011_auto_20151020_0016	2017-11-13 20:05:38.289672+00
243	membership	0012_members_group	2017-11-13 20:05:38.837787+00
244	membership	0013_auto_20151219_1510	2017-11-13 20:05:39.000034+00
245	membership	0014_term_payment_type	2017-11-13 20:05:39.180957+00
246	mimicon2016	0001_initial	2017-11-13 20:05:39.670441+00
247	mimicon2016	0002_auto_20160222_2108	2017-11-13 20:05:39.844194+00
248	mimicon2016	0003_auto_20160306_1125	2017-11-13 20:05:40.038594+00
249	mimicon2016	0004_signupextra_is_active	2017-11-13 20:05:40.225874+00
250	mimicon2016	0005_auto_20171113_2158	2017-11-13 20:05:40.650058+00
251	nexmo	0001_initial	2017-11-13 20:05:40.73662+00
252	nippori2017	0001_initial	2017-11-13 20:05:40.926986+00
253	oauth2_provider	0001_initial	2017-11-13 20:05:41.706348+00
254	oauth2_provider	0002_08_updates	2017-11-13 20:05:42.373527+00
255	oauth2_provider	0003_auto_20160316_1503	2017-11-13 20:05:42.657618+00
256	oauth2_provider	0004_auto_20160525_1623	2017-11-13 20:05:43.19873+00
257	payments	0001_initial	2017-11-13 20:05:43.216704+00
258	payments	0002_paymentseventmeta	2017-11-13 20:05:43.535532+00
259	payments	0003_payment_event	2017-11-13 20:05:43.717035+00
260	popcult2017	0001_initial	2017-11-13 20:05:43.926643+00
261	popcult2017	0002_auto_20170417_2259	2017-11-13 20:05:44.247824+00
262	programme	0001_initial	2017-11-13 20:05:47.465057+00
263	programme	0002_auto_20150115_1949	2017-11-13 20:05:47.938116+00
264	programme	0003_programme_state	2017-11-13 20:05:48.467083+00
265	programme	0004_auto_20151024_1644	2017-11-13 20:05:48.649018+00
266	programme	0005_programme_end_time	2017-11-13 20:05:49.128642+00
267	programme	0006_room_slug	2017-11-13 20:05:49.493346+00
268	programme	0007_room_slug_not_null	2017-11-13 20:05:49.803257+00
269	programme	0008_category_slug	2017-11-13 20:05:50.331497+00
270	programme	0009_auto_20160123_1336	2017-11-13 20:05:52.176328+00
271	programme	0010_auto_20160123_1733	2017-11-13 20:05:53.334445+00
272	programme	0011_auto_20160124_1448	2017-11-13 20:05:54.653642+00
273	programme	0012_auto_20160124_1457	2017-11-13 20:05:55.333258+00
274	programme	0013_auto_20160124_2151	2017-11-13 20:05:55.688799+00
275	programme	0014_invitationadminproxy_programmemanagementproxy	2017-11-13 20:05:55.706993+00
276	programme	0015_auto_20160125_2328	2017-11-13 20:05:58.655821+00
277	programme	0016_freeformorganizer	2017-11-13 20:05:58.863283+00
278	programme	0017_freeformorganizeradminproxy	2017-11-13 20:05:58.875433+00
279	programme	0018_auto_20160131_2044	2017-11-13 20:05:59.529324+00
280	programme	0019_auto_20160201_0003	2017-11-13 20:06:00.171075+00
281	programme	0020_make_role_event_specific	2017-11-13 20:06:00.188982+00
282	programme	0021_auto_20160201_0050	2017-11-13 20:06:00.422201+00
283	programme	0022_auto_20160202_1950	2017-11-13 20:06:00.911002+00
284	programme	0023_auto_20160202_2231	2017-11-13 20:06:01.544603+00
285	programme	0024_auto_20160202_2236	2017-11-13 20:06:02.187608+00
286	programme	0025_auto_20160202_2237	2017-11-13 20:06:02.199203+00
287	programme	0026_auto_20160202_2238	2017-11-13 20:06:02.405292+00
288	programme	0027_auto_20160204_1842	2017-11-13 20:06:04.214947+00
289	programme	0028_auto_20160207_2330	2017-11-13 20:06:05.470755+00
290	programme	0029_room_active	2017-11-13 20:06:05.683801+00
291	programme	0030_auto_20160305_1902	2017-11-13 20:06:06.401952+00
292	programme	0031_auto_20160306_1125	2017-11-13 20:06:06.596438+00
293	programme	0032_auto_20160505_2233	2017-11-13 20:06:06.902629+00
294	programme	0033_auto_20160608_0023	2017-11-13 20:06:07.103629+00
295	programme	0034_auto_20160608_2309	2017-11-13 20:06:07.304999+00
296	programme	0035_auto_20160623_0037	2017-11-13 20:06:07.9597+00
297	programme	0036_programme_frozen	2017-11-13 20:06:08.178279+00
298	programme	0037_populate_programme_frozen	2017-11-13 20:06:08.194754+00
299	programme	0038_auto_20160627_2057	2017-11-13 20:06:08.515337+00
300	programme	0039_programmefeedback	2017-11-13 20:06:08.736534+00
301	programme	0040_auto_20160705_2240	2017-11-13 20:06:09.259301+00
302	programme	0041_programme_rerun	2017-11-13 20:06:09.475521+00
303	programme	0042_auto_20160706_2208	2017-11-13 20:06:09.681064+00
304	programme	0043_auto_20160706_2211	2017-11-13 20:06:10.001629+00
305	programme	0044_auto_20160712_1406	2017-11-13 20:06:10.660968+00
306	programme	0045_auto_20160715_0127	2017-11-13 20:06:11.061116+00
307	programme	0046_auto_20160811_2319	2017-11-13 20:06:11.567905+00
308	programme	0047_programmeeventmeta_schedule_layout	2017-11-13 20:06:11.79339+00
309	programme	0048_auto_20160813_1948	2017-11-13 20:06:12.105886+00
310	programme	0049_programmerole_is_active	2017-11-13 20:06:12.342929+00
311	programme	0050_auto_20161129_2147	2017-11-13 20:06:16.262469+00
312	programme	0051_auto_20170212_2203	2017-11-13 20:06:16.473496+00
313	programme	0052_tag_slug	2017-11-13 20:06:16.677098+00
314	programme	0053_populate_tag_slug	2017-11-13 20:06:16.688101+00
315	programme	0054_auto_20170212_2334	2017-11-13 20:06:17.00181+00
316	programme	0055_programme_signup_link	2017-11-13 20:06:17.236219+00
317	programme	0056_auto_20171104_1806	2017-11-13 20:06:17.913142+00
318	programme	0057_room_event	2017-11-13 20:06:18.642236+00
319	programme	0058_populate_room_event	2017-11-13 20:06:18.658181+00
320	programme	0059_room_remove_venue	2017-11-13 20:06:19.035708+00
321	programme	0060_auto_20171113_2158	2017-11-13 20:06:19.53286+00
322	sessions	0001_initial	2017-11-13 20:06:19.553174+00
323	shippocon2016	0001_initial	2017-11-13 20:06:20.123225+00
324	shippocon2016	0002_auto_20171113_2158	2017-11-13 20:06:21.629868+00
325	sites	0001_initial	2017-11-13 20:06:21.651387+00
326	sites	0002_alter_domain_unique	2017-11-13 20:06:21.67349+00
327	sms	0001_initial	2017-11-13 20:06:23.592528+00
328	sms	0002_refactor_smsevent	2017-11-13 20:06:24.866355+00
329	sms	0003_refactoring	2017-11-13 20:06:26.509655+00
330	sms	0004_vote_has_nominee_not_another_way_round	2017-11-13 20:06:26.989327+00
331	sms	0005_review	2017-11-13 20:06:27.500807+00
332	tickets	0001_initial	2017-11-13 20:06:29.254466+00
333	tickets	0002_ticketseventmeta_front_page_text	2017-11-13 20:06:29.581766+00
334	tickets	0003_auto_20141201_0013	2017-11-13 20:06:29.803429+00
335	tickets	0004_auto_20150125_1601	2017-11-13 20:06:30.025521+00
336	tickets	0005_auto_20150208_1455	2017-11-13 20:06:30.796388+00
337	tickets	0006_ticketseventmeta_receipt_footer	2017-11-13 20:06:31.157677+00
338	tickets	0007_accommodation_v3	2017-11-13 20:06:31.599652+00
339	tickets	0008_auto_20151108_1905	2017-11-13 20:06:32.129523+00
340	tickets	0009_accom_limit_group_refactor	2017-11-13 20:06:32.723997+00
341	tickets	0010_product_requires_shirt_size	2017-11-13 20:06:32.963004+00
342	tickets	0011_auto_20160216_2116	2017-11-13 20:06:33.679912+00
343	tickets	0012_shirtorder	2017-11-13 20:06:33.930802+00
344	tickets	0013_auto_20160216_2208	2017-11-13 20:06:34.948287+00
345	tickets	0014_auto_20160305_1902	2017-11-13 20:06:35.445959+00
346	tickets	0015_auto_20160608_0023	2017-11-13 20:06:35.845012+00
347	tickets	0016_remove_ticketseventmeta_plain_contact_email	2017-11-13 20:06:36.105332+00
348	tickets	0017_auto_20160608_2309	2017-11-13 20:06:36.364738+00
349	tickets	0018_auto_20160610_0005	2017-11-13 20:06:37.410523+00
350	tickets	0019_auto_20160704_2222	2017-11-13 20:06:37.679457+00
351	tickets	0020_auto_20160706_2207	2017-11-13 20:06:37.950467+00
352	tickets	0021_auto_20161211_1549	2017-11-13 20:06:45.296563+00
353	tickets	0022_orderproduct_unique_together	2017-11-13 20:06:45.538859+00
354	tracon11	0001_initial	2017-11-13 20:06:46.254939+00
355	tracon11	0002_auto_20160306_1125	2017-11-13 20:06:46.581536+00
356	tracon11	0003_signupextra_is_active	2017-11-13 20:06:46.958728+00
357	tracon11	0004_auto_20160716_1419	2017-11-13 20:06:47.748546+00
358	tracon11	0005_auto_20160804_0035	2017-11-13 20:06:47.994842+00
359	tracon11	0006_signupextrav2	2017-11-13 20:06:48.39514+00
360	tracon11	0007_migrate_to_signupextrav2	2017-11-13 20:06:48.408212+00
361	tracon11	0008_auto_20160901_2351	2017-11-13 20:06:49.21982+00
362	tracon11	0009_auto_20160912_2125	2017-11-13 20:06:49.481643+00
363	tracon11	0010_delete_signupextrav2afterpartyproxy	2017-11-13 20:06:49.492572+00
364	tracon2017	0001_initial	2017-11-13 20:06:49.887905+00
365	tracon2017	0002_auto_20170911_2256	2017-11-13 20:06:50.973711+00
366	tracon2017	0003_auto_20170912_2259	2017-11-13 20:06:51.373037+00
367	tracon2017	0004_auto_20171113_2158	2017-11-13 20:06:51.638737+00
368	tracon2018	0001_initial	2017-11-13 20:06:51.930703+00
369	tracon9	0001_initial	2017-11-13 20:06:52.605496+00
370	tracon9	0002_auto_20160306_1125	2017-11-13 20:06:52.98691+00
371	tracon9	0003_signupextra_is_active	2017-11-13 20:06:53.259938+00
372	tracon9	0004_auto_20171113_2158	2017-11-13 20:06:53.857463+00
373	traconx	0001_initial	2017-11-13 20:06:54.533432+00
374	traconx	0002_signupextra_email_alias	2017-11-13 20:06:54.797338+00
375	traconx	0003_auto_20141207_1557	2017-11-13 20:06:55.172597+00
376	traconx	0004_auto_20150419_1514	2017-11-13 20:06:55.767033+00
377	traconx	0005_auto_20150521_1557	2017-11-13 20:06:56.026116+00
378	traconx	0006_auto_20160306_1125	2017-11-13 20:06:56.317712+00
379	traconx	0007_signupextra_is_active	2017-11-13 20:06:56.720428+00
380	traconx	0008_auto_20171113_2158	2017-11-13 20:06:57.327355+00
381	tylycon2017	0001_initial	2017-11-13 20:06:57.978711+00
382	tylycon2017	0002_auto_20161006_1243	2017-11-13 20:06:58.231241+00
383	tylycon2017	0003_signupextra_motivation	2017-11-13 20:06:58.512289+00
384	tylycon2017	0004_auto_20161020_1850	2017-11-13 20:06:59.159694+00
385	tylycon2017	0005_auto_20171113_2158	2017-11-13 20:06:59.755261+00
386	worldcon75	0001_initial	2017-11-13 20:07:00.166412+00
387	yukicon2016	0001_initial	2017-11-13 20:07:00.81639+00
388	yukicon2016	0002_auto_20151107_1903	2017-11-13 20:07:01.075887+00
389	yukicon2016	0003_auto_20151109_0912	2017-11-13 20:07:01.355064+00
390	yukicon2016	0004_auto_20160306_1125	2017-11-13 20:07:01.774951+00
391	yukicon2016	0005_signupextra_is_active	2017-11-13 20:07:02.051695+00
392	yukicon2016	0006_auto_20171113_2158	2017-11-13 20:07:02.656895+00
393	yukicon2017	0001_initial	2017-11-13 20:07:03.762618+00
394	yukicon2017	0002_auto_20160921_2248	2017-11-13 20:07:04.075293+00
395	yukicon2017	0003_remove_signupextra_shirt_size	2017-11-13 20:07:04.359894+00
396	yukicon2017	0004_auto_20171113_2158	2017-11-13 20:07:05.402629+00
397	yukicon2018	0001_initial	2017-11-13 20:07:06.339953+00
398	yukicon2018	0002_auto_20170824_2310	2017-11-13 20:07:06.982483+00
399	yukicon2018	0003_auto_20170824_2323	2017-11-13 20:07:07.383916+00
400	aicon2018	0001_initial	2018-09-16 07:29:07.681724+00
401	desucon2018	0001_initial	2018-09-16 07:29:08.306587+00
402	desucon2018	0002_signupextra_afterparty_participation	2018-09-16 07:29:08.622882+00
403	desucon2019	0001_initial	2018-09-16 07:29:09.218347+00
404	finncon2018	0001_initial	2018-09-16 07:29:09.696189+00
405	finncon2018	0002_auto_20180429_2012	2018-09-16 07:29:10.219468+00
406	finncon2018	0003_auto_20180611_1943	2018-09-16 07:29:10.731831+00
407	frostbite2018	0002_auto_20171225_1335	2018-09-16 07:29:11.043076+00
408	frostbite2019	0001_initial	2018-09-16 07:29:11.634745+00
409	listings	0001_initial	2018-09-16 07:29:11.890828+00
410	listings	0002_listing_external_events	2018-09-16 07:29:12.218519+00
411	listings	0003_externalevent_public	2018-09-16 07:29:12.46271+00
412	listings	0004_externalevent_logo_file	2018-09-16 07:29:12.795301+00
413	matsucon2018	0001_initial	2018-09-16 07:29:13.062045+00
414	matsucon2018	0002_auto_20180203_2326	2018-09-16 07:29:14.493801+00
415	matsucon2018	0003_signupextra_shirt_size	2018-09-16 07:29:14.785035+00
416	matsucon2018	0004_signupextra_shift_type	2018-09-16 07:29:15.122643+00
417	mimicon2018	0001_initial	2018-09-16 07:29:15.74708+00
418	popcultday2018	0001_initial	2018-09-16 07:29:15.9995+00
419	ropecon2018	0001_initial	2018-09-16 07:29:16.741353+00
420	programme	0061_auto_20171125_1229	2018-09-16 07:29:17.375348+00
421	programme	0062_populate_viewroom	2018-09-16 07:29:17.390861+00
422	programme	0063_remove_view_rooms	2018-09-16 07:29:17.638765+00
423	programme	0064_auto_20171125_1326	2018-09-16 07:29:18.224015+00
424	programme	0065_auto_20171227_0037	2018-09-16 07:29:20.381756+00
425	programme	0066_programme_ropecon2018_preferred_time_slots	2018-09-16 07:29:20.645663+00
426	programme	0067_auto_20180219_2222	2018-09-16 07:29:21.2733+00
427	programme	0068_auto_20180305_2153	2018-09-16 07:29:29.200183+00
428	programme	0069_ropecon2018_kp_20180306_0934	2018-09-16 07:29:30.170737+00
429	programme	0070_auto_20180307_2316	2018-09-16 07:29:30.427426+00
430	programme	0071_auto_20180417_2245	2018-09-16 07:29:31.916846+00
431	programme	0072_programme_language_skills	2018-09-16 07:29:32.174569+00
432	programme	0073_remove_programme_language_skills	2018-09-16 07:29:32.525434+00
433	programme	0074_auto_20180620_1623	2018-09-16 07:29:32.768979+00
434	ropecon2018	0002_remove_signupextra_extra_work	2018-09-16 07:29:33.099862+00
435	surveys	0003_auto_20180330_1812	2018-09-16 07:29:33.708228+00
436	tickets	0023_auto_20180212_2301	2018-09-16 07:29:34.296714+00
437	tickets	0024_ticketseventmeta_pos_access_group	2018-09-16 07:29:34.536896+00
438	tracon2018	0002_auto_20180913_0813	2018-09-16 07:29:36.659198+00
439	yukicon2019	0001_initial	2018-09-16 07:29:37.68993+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: enrollment_conconpart; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_conconpart (id, name) FROM stdin;
\.


--
-- Data for Name: enrollment_enrollment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_enrollment (id, special_diet_other, event_id, person_id, concon_event_affiliation, created_at, is_public, state, updated_at) FROM stdin;
\.


--
-- Data for Name: enrollment_enrollment_concon_parts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_enrollment_concon_parts (id, enrollment_id, conconpart_id) FROM stdin;
\.


--
-- Data for Name: enrollment_enrollment_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_enrollment_special_diet (id, enrollment_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: enrollment_enrollmenteventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_enrollmenteventmeta (event_id, form_class_path, enrollment_opens, enrollment_closes, admin_group_id, override_enrollment_form_message, initial_state, is_participant_list_public) FROM stdin;
\.


--
-- Data for Name: enrollment_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.enrollment_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: event_log_entry; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.event_log_entry (id, created_at, entry_type, created_by_id, feedback_message_id, event_id, event_survey_result_id, global_survey_result_id, context, person_id, organization_id, search_term, ip_address) FROM stdin;
\.


--
-- Data for Name: event_log_subscription; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.event_log_subscription (id, entry_type, channel, active, user_id, callback_code, event_filter_id, event_survey_filter_id) FROM stdin;
\.


--
-- Data for Name: feedback_feedbackmessage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.feedback_feedbackmessage (id, context, author_ip_address, feedback, created_at, author_id) FROM stdin;
\.


--
-- Data for Name: finncon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2016_signupextra (signup_id, shift_type, total_work, special_diet_other, prior_experience, free_text, dead_dog, shirt_size, is_active) FROM stdin;
\.


--
-- Data for Name: finncon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: finncon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: finncon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2018_signupextra (signup_id, is_active, shift_type, total_work, shirt_size, dead_dog, special_diet_other, prior_experience, free_text, language_skills) FROM stdin;
\.


--
-- Data for Name: finncon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: finncon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.finncon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: frostbite2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2016_signupextra (signup_id, shift_type, desu_amount, prior_experience, free_text, shirt_size, shirt_type, night_work, is_active) FROM stdin;
\.


--
-- Data for Name: frostbite2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2017_signupextra (id, is_active, shift_type, desu_amount, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: frostbite2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: frostbite2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: frostbite2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2018_signupextra (id, is_active, shift_type, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: frostbite2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: frostbite2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: frostbite2019_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2019_signupextra (id, is_active, shift_type, prior_experience, free_text, special_diet_other, shirt_size, shirt_type, night_work, afterparty_participation, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: frostbite2019_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2019_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: frostbite2019_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.frostbite2019_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: hitpoint2015_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2015_signupextra (signup_id, shift_type, total_work, construction, overseer, want_certificate, certificate_delivery_address, special_diet_other, prior_experience, free_text, night_work, shift_wishes, need_lodging, is_active) FROM stdin;
\.


--
-- Data for Name: hitpoint2015_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2015_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: hitpoint2015_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2015_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: hitpoint2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2017_signupextra (signup_id, shift_type, total_work, night_work, construction, overseer, want_certificate, certificate_delivery_address, special_diet_other, need_lodging, prior_experience, shift_wishes, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: hitpoint2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: hitpoint2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: hitpoint2017_timeslot; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hitpoint2017_timeslot (id, name) FROM stdin;
\.


--
-- Data for Name: intra_intraeventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.intra_intraeventmeta (event_id, admin_group_id, organizer_group_id) FROM stdin;
\.


--
-- Data for Name: intra_team; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.intra_team (id, "order", name, description, slug, event_id, group_id, email) FROM stdin;
\.


--
-- Data for Name: intra_teammember; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.intra_teammember (id, is_primary_team, is_team_leader, is_shown_internally, is_shown_publicly, is_group_member, person_id, team_id, override_name_display_style, override_job_title) FROM stdin;
\.


--
-- Data for Name: kawacon2016_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2016_night (id, name) FROM stdin;
\.


--
-- Data for Name: kawacon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2016_signupextra (signup_id, shirt_size, special_diet_other, prior_experience, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: kawacon2016_signupextra_needs_lodging; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2016_signupextra_needs_lodging (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: kawacon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kawacon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: kawacon2017_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_night (id, name) FROM stdin;
\.


--
-- Data for Name: kawacon2017_shift; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_shift (id, name) FROM stdin;
\.


--
-- Data for Name: kawacon2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_signupextra (id, is_active, shirt_size, special_diet_other, afterparty, prior_experience, free_text, event_id, person_id, want_certificate) FROM stdin;
\.


--
-- Data for Name: kawacon2017_signupextra_needs_lodging; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_signupextra_needs_lodging (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: kawacon2017_signupextra_shifts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_signupextra_shifts (id, signupextra_id, shift_id) FROM stdin;
\.


--
-- Data for Name: kawacon2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kawacon2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kawacon2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: kuplii2015_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2015_signupextra (signup_id, shift_type, total_work, special_diet_other, prior_experience, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: kuplii2015_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2015_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kuplii2015_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2015_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: kuplii2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2016_signupextra (signup_id, shift_type, total_work, special_diet_other, prior_experience, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: kuplii2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kuplii2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: kuplii2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2017_signupextra (id, is_active, shift_type, total_work, special_diet_other, prior_experience, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: kuplii2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kuplii2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: kuplii2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2018_signupextra (id, is_active, shift_type, total_work, special_diet_other, prior_experience, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: kuplii2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: kuplii2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.kuplii2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: labour_alternativesignupform; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_alternativesignupform (id, slug, title, signup_form_class_path, signup_extra_form_class_path, active_from, active_until, signup_message, event_id) FROM stdin;
\.


--
-- Data for Name: labour_common_qualifications_jvkortti; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_common_qualifications_jvkortti (personqualification_id, card_number, expiration_date) FROM stdin;
\.


--
-- Data for Name: labour_emptysignupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_emptysignupextra (id, event_id, person_id, is_active) FROM stdin;
\.


--
-- Data for Name: labour_infolink; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_infolink (id, url, title, event_id, group_id) FROM stdin;
\.


--
-- Data for Name: labour_job; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_job (id, title, job_category_id, slug) FROM stdin;
\.


--
-- Data for Name: labour_jobcategory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_jobcategory (id, name, slug, description, public, event_id, app_label) FROM stdin;
\.


--
-- Data for Name: labour_jobcategory_personnel_classes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_jobcategory_personnel_classes (id, jobcategory_id, personnelclass_id) FROM stdin;
\.


--
-- Data for Name: labour_jobcategory_required_qualifications; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_jobcategory_required_qualifications (id, jobcategory_id, qualification_id) FROM stdin;
\.


--
-- Data for Name: labour_jobrequirement; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_jobrequirement (id, count, start_time, end_time, job_id) FROM stdin;
\.


--
-- Data for Name: labour_laboureventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_laboureventmeta (event_id, registration_opens, registration_closes, work_begins, work_ends, monitor_email, contact_email, signup_message, admin_group_id, signup_extra_content_type_id, work_certificate_signer) FROM stdin;
\.


--
-- Data for Name: labour_obsoleteemptysignupextrav1; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_obsoleteemptysignupextrav1 (signup_id, is_active) FROM stdin;
\.


--
-- Data for Name: labour_perk; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_perk (id, slug, name, event_id) FROM stdin;
\.


--
-- Data for Name: labour_personnelclass; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_personnelclass (id, app_label, name, slug, priority, event_id, icon_css_class) FROM stdin;
\.


--
-- Data for Name: labour_personnelclass_perks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_personnelclass_perks (id, personnelclass_id, perk_id) FROM stdin;
\.


--
-- Data for Name: labour_personqualification; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_personqualification (id, person_id, qualification_id) FROM stdin;
\.


--
-- Data for Name: labour_qualification; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_qualification (id, slug, name, description, qualification_extra_content_type_id) FROM stdin;
\.


--
-- Data for Name: labour_shift; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_shift (id, start_time, hours, notes, job_id, signup_id) FROM stdin;
\.


--
-- Data for Name: labour_signup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_signup (id, notes, created_at, updated_at, xxx_interim_shifts, job_title, is_active, time_accepted, time_finished, time_complained, time_cancelled, time_rejected, time_arrived, time_work_accepted, time_reprimanded, alternative_signup_form_used_id, event_id, person_id, time_confirmation_requested) FROM stdin;
\.


--
-- Data for Name: labour_signup_job_categories; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_signup_job_categories (id, signup_id, jobcategory_id) FROM stdin;
\.


--
-- Data for Name: labour_signup_job_categories_accepted; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_signup_job_categories_accepted (id, signup_id, jobcategory_id) FROM stdin;
\.


--
-- Data for Name: labour_signup_job_categories_rejected; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_signup_job_categories_rejected (id, signup_id, jobcategory_id) FROM stdin;
\.


--
-- Data for Name: labour_signup_personnel_classes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_signup_personnel_classes (id, signup_id, personnelclass_id) FROM stdin;
\.


--
-- Data for Name: labour_survey; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_survey (id, slug, title, description, active_from, active_until, form_class_path, event_id, override_does_not_apply_message) FROM stdin;
\.


--
-- Data for Name: labour_surveyrecord; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_surveyrecord (id, created_at, updated_at, person_id, survey_id) FROM stdin;
\.


--
-- Data for Name: labour_workperiod; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.labour_workperiod (id, description, start_time, end_time, event_id) FROM stdin;
\.


--
-- Data for Name: lakeuscon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lakeuscon2016_signupextra (signup_id, shift_type, shirt_size, special_diet_other, prior_experience, shift_wishes, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: lakeuscon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lakeuscon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: lakeuscon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lakeuscon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: lippukala_code; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lippukala_code (id, created_on, status, used_on, used_at, prefix, code, literate_code, product_text, order_id) FROM stdin;
\.


--
-- Data for Name: lippukala_order; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.lippukala_order (id, event, created_on, modified_on, reference_number, address_text, free_text, comment) FROM stdin;
\.


--
-- Data for Name: listings_externalevent; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.listings_externalevent (id, slug, name, description, homepage_url, venue_name, start_time, end_time, public, logo_file) FROM stdin;
\.


--
-- Data for Name: listings_listing; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.listings_listing (id, hostname, title, description) FROM stdin;
\.


--
-- Data for Name: listings_listing_events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.listings_listing_events (id, listing_id, event_id) FROM stdin;
\.


--
-- Data for Name: listings_listing_external_events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.listings_listing_external_events (id, listing_id, externalevent_id) FROM stdin;
\.


--
-- Data for Name: mailings_message; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mailings_message (id, subject_template, body_template, created_at, updated_at, sent_at, expired_at, recipient_id, channel) FROM stdin;
\.


--
-- Data for Name: mailings_personmessage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mailings_personmessage (id, created_at, body_id, message_id, person_id, subject_id) FROM stdin;
\.


--
-- Data for Name: mailings_personmessagebody; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mailings_personmessagebody (id, digest, text) FROM stdin;
\.


--
-- Data for Name: mailings_personmessagesubject; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mailings_personmessagesubject (id, digest, text) FROM stdin;
\.


--
-- Data for Name: mailings_recipientgroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mailings_recipientgroup (id, app_label, verbose_name, event_id, group_id, job_category_id, personnel_class_id) FROM stdin;
\.


--
-- Data for Name: matsucon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matsucon2018_signupextra (id, is_active, want_certificate, special_diet_other, prior_experience, free_text, event_id, person_id, more_info, need_lodging, night_work, shirt_size, shift_type) FROM stdin;
\.


--
-- Data for Name: matsucon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.matsucon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: membership_membership; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.membership_membership (id, organization_id, person_id, state, message) FROM stdin;
\.


--
-- Data for Name: membership_membershipfeepayment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.membership_membershipfeepayment (id, payment_date, member_id, term_id) FROM stdin;
\.


--
-- Data for Name: membership_membershiporganizationmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.membership_membershiporganizationmeta (organization_id, admin_group_id, receiving_applications, membership_requirements, members_group_id) FROM stdin;
\.


--
-- Data for Name: membership_term; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.membership_term (id, title, start_date, end_date, entrance_fee_cents, membership_fee_cents, organization_id, payment_type) FROM stdin;
\.


--
-- Data for Name: mimicon2016_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2016_night (id, name) FROM stdin;
\.


--
-- Data for Name: mimicon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2016_signupextra (signup_id, shift_type, total_work, construction, want_certificate, special_diet_other, prior_experience, shift_wishes, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: mimicon2016_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2016_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: mimicon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: mimicon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: mimicon2018_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2018_night (id, name) FROM stdin;
\.


--
-- Data for Name: mimicon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2018_signupextra (signup_id, is_active, shift_type, total_work, construction, want_certificate, special_diet_other, prior_experience, shift_wishes, free_text) FROM stdin;
\.


--
-- Data for Name: mimicon2018_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2018_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: mimicon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: mimicon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.mimicon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: nexmo_deliverystatusfragment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.nexmo_deliverystatusfragment (id, nexmo_message_id, error_code, status_msg, status_timestamp, message_id) FROM stdin;
\.


--
-- Data for Name: nexmo_inboundmessage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.nexmo_inboundmessage (id, nexmo_message_id, sender, nexmo_timestamp, receive_timestamp, message) FROM stdin;
\.


--
-- Data for Name: nexmo_inboundmessagefragment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.nexmo_inboundmessagefragment (id, nexmo_message_id, sender, nexmo_timestamp, receive_timestamp, message, concat_ref, concat_part, concat_total) FROM stdin;
\.


--
-- Data for Name: nexmo_outboundmessage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.nexmo_outboundmessage (id, message, "to", send_timestamp, send_status, status, sent_pieces, external_reference) FROM stdin;
\.


--
-- Data for Name: nippori2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.nippori2017_signupextra (id, is_active, prior_experience, shift_wishes, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: oauth2_provider_accesstoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.oauth2_provider_accesstoken (id, token, expires, scope, application_id, user_id) FROM stdin;
\.


--
-- Data for Name: oauth2_provider_application; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, user_id, skip_authorization) FROM stdin;
\.


--
-- Data for Name: oauth2_provider_grant; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.oauth2_provider_grant (id, code, expires, redirect_uri, scope, application_id, user_id) FROM stdin;
\.


--
-- Data for Name: oauth2_provider_refreshtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.oauth2_provider_refreshtoken (id, token, access_token_id, application_id, user_id) FROM stdin;
\.


--
-- Data for Name: payments_payment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payments_payment (id, test, "VERSION", "STAMP", "REFERENCE", "PAYMENT", "STATUS", "ALGORITHM", "MAC", event_id) FROM stdin;
\.


--
-- Data for Name: payments_paymentseventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payments_paymentseventmeta (event_id, checkout_password, checkout_merchant, checkout_delivery_date, admin_group_id) FROM stdin;
\.


--
-- Data for Name: popcult2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.popcult2017_signupextra (id, is_active, want_certificate, special_diet_other, y_u, prior_experience, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: popcult2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.popcult2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: popcultday2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.popcultday2018_signupextra (id, is_active, want_certificate, special_diet_other, y_u, prior_experience, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: popcultday2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.popcultday2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: programme_alternativeprogrammeform; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_alternativeprogrammeform (id, slug, title, description, short_description, programme_form_code, active_from, active_until, num_extra_invites, "order", event_id) FROM stdin;
\.


--
-- Data for Name: programme_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_category (id, title, style, notes, public, event_id, slug) FROM stdin;
\.


--
-- Data for Name: programme_freeformorganizer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_freeformorganizer (id, text, programme_id) FROM stdin;
\.


--
-- Data for Name: programme_invitation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_invitation (id, email, programme_id, role_id, code, created_at, state, used_at, created_by_id, extra_invites, sire_id) FROM stdin;
\.


--
-- Data for Name: programme_programme; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programme (id, title, description, room_requirements, tech_requirements, requested_time_slot, video_permission, notes_from_host, start_time, length, notes, category_id, room_id, state, end_time, created_at, updated_at, slug, computer, encumbered_content, number_of_microphones, photography, use_audio, use_video, frozen, video_link, rerun, approximate_length, is_age_restricted, is_beginner_friendly, is_children_friendly, is_english_ok, is_intended_for_experienced_participants, max_players, min_players, other_author, physical_play, rpg_system, three_word_description, form_used_id, signup_link, length_from_host, long_description, ropecon2018_audience_size, ropecon2018_characters, ropecon2018_genre_drama, ropecon2018_genre_exploration, ropecon2018_genre_fantasy, ropecon2018_genre_historical, ropecon2018_genre_horror, ropecon2018_genre_humor, ropecon2018_genre_modern, ropecon2018_genre_mystery, ropecon2018_genre_scifi, ropecon2018_genre_war, ropecon2018_is_no_language, ropecon2018_is_panel_attendance_ok, ropecon2018_prop_requirements, ropecon2018_sessions, ropecon2018_signuplist, ropecon2018_space_requirements, ropecon2018_speciality, ropecon2018_style_character_driven, ropecon2018_style_combat_driven, ropecon2018_style_light, ropecon2018_style_rules_heavy, ropecon2018_style_rules_light, ropecon2018_style_serious, ropecon2018_style_story_driven, ropecon2018_kp_difficulty, ropecon2018_kp_length, ropecon2018_kp_tables, language) FROM stdin;
\.


--
-- Data for Name: programme_programme_hitpoint2017_preferred_time_slots; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programme_hitpoint2017_preferred_time_slots (id, programme_id, timeslot_id) FROM stdin;
\.


--
-- Data for Name: programme_programme_ropecon2018_preferred_time_slots; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programme_ropecon2018_preferred_time_slots (id, programme_id, timeslot_id) FROM stdin;
\.


--
-- Data for Name: programme_programme_tags; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programme_tags (id, programme_id, tag_id) FROM stdin;
\.


--
-- Data for Name: programme_programmeeventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programmeeventmeta (event_id, contact_email, admin_group_id, public_from, accepting_cold_offers_from, accepting_cold_offers_until, schedule_layout) FROM stdin;
\.


--
-- Data for Name: programme_programmefeedback; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programmefeedback (id, author_ip_address, is_anonymous, feedback, created_at, hidden_at, author_id, hidden_by_id, programme_id) FROM stdin;
\.


--
-- Data for Name: programme_programmerole; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_programmerole (id, person_id, programme_id, role_id, invitation_id, extra_invites, is_active) FROM stdin;
\.


--
-- Data for Name: programme_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_role (id, title, require_contact_info, is_default, is_public, personnel_class_id, priority, override_public_title) FROM stdin;
\.


--
-- Data for Name: programme_room; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_room (id, name, notes, slug, event_id) FROM stdin;
\.


--
-- Data for Name: programme_specialstarttime; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_specialstarttime (id, start_time, event_id) FROM stdin;
\.


--
-- Data for Name: programme_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_tag (id, title, "order", style, event_id, slug) FROM stdin;
\.


--
-- Data for Name: programme_timeblock; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_timeblock (id, start_time, end_time, event_id) FROM stdin;
\.


--
-- Data for Name: programme_view; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_view (id, name, public, "order", event_id, end_time, start_time) FROM stdin;
\.


--
-- Data for Name: programme_viewroom; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.programme_viewroom (id, "order", room_id, view_id) FROM stdin;
\.


--
-- Data for Name: ropecon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ropecon2018_signupextra (signup_id, shift_type, total_work, want_certificate, certificate_delivery_address, special_diet_other, prior_experience, shift_wishes, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: ropecon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ropecon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: ropecon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ropecon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: ropecon2018_timeslot; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ropecon2018_timeslot (id, name) FROM stdin;
\.


--
-- Data for Name: shippocon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.shippocon2016_signupextra (id, is_active, special_diet_other, total_work, shift_type, working_days, prior_experience, shift_wishes, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: shippocon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.shippocon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: shippocon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.shippocon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: sms_hotword; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_hotword (id, hotword, slug, valid_from, valid_to, assigned_event_id) FROM stdin;
\.


--
-- Data for Name: sms_nominee; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_nominee (id, number, name) FROM stdin;
\.


--
-- Data for Name: sms_nominee_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_nominee_category (id, nominee_id, votecategory_id) FROM stdin;
\.


--
-- Data for Name: sms_smseventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_smseventmeta (event_id, sms_enabled, current, used_credit, admin_group_id) FROM stdin;
\.


--
-- Data for Name: sms_smsmessagein; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_smsmessagein (id, message_id, "SMSEventMeta_id") FROM stdin;
\.


--
-- Data for Name: sms_smsmessageout; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_smsmessageout (id, message, "to", event_id, ref_id) FROM stdin;
\.


--
-- Data for Name: sms_vote; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_vote (id, vote_id, category_id, message_id) FROM stdin;
\.


--
-- Data for Name: sms_votecategory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sms_votecategory (id, category, slug, "primary", hotword_id) FROM stdin;
\.


--
-- Data for Name: surveys_eventsurvey; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.surveys_eventsurvey (id, title, description, is_active, created_at, updated_at, model, slug, event_id, owner_id) FROM stdin;
\.


--
-- Data for Name: surveys_eventsurveyresult; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.surveys_eventsurveyresult (id, created_at, model, author_ip_address, author_id, survey_id) FROM stdin;
\.


--
-- Data for Name: surveys_globalsurvey; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.surveys_globalsurvey (id, title, description, is_active, created_at, updated_at, model, slug, owner_id) FROM stdin;
\.


--
-- Data for Name: surveys_globalsurveyresult; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.surveys_globalsurveyresult (id, created_at, model, author_ip_address, author_id, survey_id) FROM stdin;
\.


--
-- Data for Name: tickets_accommodationinformation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_accommodationinformation (id, first_name, last_name, phone_number, email, order_product_id) FROM stdin;
\.


--
-- Data for Name: tickets_accommodationinformation_limit_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_accommodationinformation_limit_groups (id, accommodationinformation_id, limitgroup_id) FROM stdin;
\.


--
-- Data for Name: tickets_batch; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_batch (id, create_time, delivery_time, event_id) FROM stdin;
\.


--
-- Data for Name: tickets_customer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_customer (id, first_name, last_name, address, zip_code, city, email, allow_marketing_email, phone_number) FROM stdin;
\.


--
-- Data for Name: tickets_limitgroup; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_limitgroup (id, description, "limit", event_id) FROM stdin;
\.


--
-- Data for Name: tickets_order; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_order (id, start_time, confirm_time, ip_address, payment_date, cancellation_time, reference_number, batch_id, customer_id, event_id) FROM stdin;
\.


--
-- Data for Name: tickets_orderproduct; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_orderproduct (id, count, order_id, product_id) FROM stdin;
\.


--
-- Data for Name: tickets_product; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_product (id, name, internal_description, description, mail_description, price_cents, requires_shipping, electronic_ticket, available, notify_email, ordering, event_id, requires_accommodation_information, requires_shirt_size, electronic_tickets_per_product, override_electronic_ticket_title) FROM stdin;
\.


--
-- Data for Name: tickets_product_limit_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_product_limit_groups (id, product_id, limitgroup_id) FROM stdin;
\.


--
-- Data for Name: tickets_shirtorder; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_shirtorder (id, count, order_id, size_id) FROM stdin;
\.


--
-- Data for Name: tickets_shirtsize; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_shirtsize (id, name, slug, available, type_id) FROM stdin;
\.


--
-- Data for Name: tickets_shirttype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_shirttype (id, name, slug, available, event_id) FROM stdin;
\.


--
-- Data for Name: tickets_ticketseventmeta; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tickets_ticketseventmeta (event_id, shipping_and_handling_cents, due_days, ticket_sales_starts, ticket_sales_ends, reference_number_template, contact_email, ticket_spam_email, reservation_seconds, ticket_free_text, admin_group_id, front_page_text, print_logo_height_mm, print_logo_path, print_logo_width_mm, receipt_footer, pos_access_group_id) FROM stdin;
\.


--
-- Data for Name: tracon11_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_night (id, name) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextra (signup_id, shift_type, total_work, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, email_alias, is_active, shift_wishes) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextrav2; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextrav2 (id, is_active, shift_type, total_work, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, shift_wishes, email_alias, event_id, person_id, afterparty_participation, outward_coach_departure_time, return_coach_departure_time, afterparty_coaches_changed) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextrav2_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextrav2_lodging_needs (id, signupextrav2_id, night_id) FROM stdin;
\.


--
-- Data for Name: tracon11_signupextrav2_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_signupextrav2_special_diet (id, signupextrav2_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tracon11_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon11_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: tracon2017_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_night (id, name) FROM stdin;
\.


--
-- Data for Name: tracon2017_poison; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_poison (id, name) FROM stdin;
\.


--
-- Data for Name: tracon2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_signupextra (id, is_active, shift_type, total_work, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, shift_wishes, email_alias, event_id, person_id, afterparty_coaches_changed, afterparty_participation, outward_coach_departure_time, return_coach_departure_time) FROM stdin;
\.


--
-- Data for Name: tracon2017_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: tracon2017_signupextra_pick_your_poison; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_signupextra_pick_your_poison (id, signupextra_id, poison_id) FROM stdin;
\.


--
-- Data for Name: tracon2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tracon2018_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_night (id, name) FROM stdin;
\.


--
-- Data for Name: tracon2018_poison; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_poison (id, name) FROM stdin;
\.


--
-- Data for Name: tracon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_signupextra (id, is_active, shift_type, total_work, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, shift_wishes, email_alias, event_id, person_id, afterparty_coaches_changed, afterparty_participation, outward_coach_departure_time, return_coach_departure_time, willing_to_bartend) FROM stdin;
\.


--
-- Data for Name: tracon2018_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: tracon2018_signupextra_pick_your_poison; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_signupextra_pick_your_poison (id, signupextra_id, poison_id) FROM stdin;
\.


--
-- Data for Name: tracon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tracon9_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon9_night (id, name) FROM stdin;
\.


--
-- Data for Name: tracon9_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon9_signupextra (signup_id, shift_type, total_work, construction, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: tracon9_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon9_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: tracon9_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon9_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tracon9_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tracon9_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: traconx_night; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.traconx_night (id, name) FROM stdin;
\.


--
-- Data for Name: traconx_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.traconx_signupextra (signup_id, shift_type, total_work, overseer, want_certificate, certificate_delivery_address, shirt_size, special_diet_other, prior_experience, free_text, email_alias, is_active) FROM stdin;
\.


--
-- Data for Name: traconx_signupextra_lodging_needs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.traconx_signupextra_lodging_needs (id, signupextra_id, night_id) FROM stdin;
\.


--
-- Data for Name: traconx_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.traconx_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: traconx_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.traconx_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: tylycon2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tylycon2017_signupextra (id, is_active, shift_type, total_work, want_certificate, special_diet_other, prior_experience, free_text, event_id, person_id, motivation, shift_cleanup, shift_setup) FROM stdin;
\.


--
-- Data for Name: tylycon2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tylycon2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: tylycon2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.tylycon2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: worldcon75_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.worldcon75_signupextra (id, is_active, special_diet_other, shift_wishes, prior_experience, free_text, is_attending_member, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: worldcon75_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.worldcon75_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: yukicon2016_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2016_signupextra (signup_id, shift_type, total_work, construction, want_certificate, shirt_size, special_diet_other, prior_experience, shift_wishes, free_text, is_active) FROM stdin;
\.


--
-- Data for Name: yukicon2016_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2016_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: yukicon2016_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2016_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2017_eventday; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2017_eventday (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2017_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2017_signupextra (id, is_active, shift_type, total_work, want_certificate, special_diet_other, prior_experience, shift_wishes, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: yukicon2017_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2017_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: yukicon2017_signupextra_work_days; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2017_signupextra_work_days (id, signupextra_id, eventday_id) FROM stdin;
\.


--
-- Data for Name: yukicon2017_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2017_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2018_eventday; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2018_eventday (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2018_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2018_signupextra (id, is_active, shift_type, total_work, want_certificate, special_diet_other, prior_experience, shift_wishes, free_text, event_id, person_id, shirt_size) FROM stdin;
\.


--
-- Data for Name: yukicon2018_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2018_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: yukicon2018_signupextra_work_days; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2018_signupextra_work_days (id, signupextra_id, eventday_id) FROM stdin;
\.


--
-- Data for Name: yukicon2018_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2018_specialdiet (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2019_eventday; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2019_eventday (id, name) FROM stdin;
\.


--
-- Data for Name: yukicon2019_signupextra; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2019_signupextra (id, is_active, shift_type, total_work, want_certificate, shirt_size, special_diet_other, prior_experience, shift_wishes, free_text, event_id, person_id) FROM stdin;
\.


--
-- Data for Name: yukicon2019_signupextra_special_diet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2019_signupextra_special_diet (id, signupextra_id, specialdiet_id) FROM stdin;
\.


--
-- Data for Name: yukicon2019_signupextra_work_days; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2019_signupextra_work_days (id, signupextra_id, eventday_id) FROM stdin;
\.


--
-- Data for Name: yukicon2019_specialdiet; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.yukicon2019_specialdiet (id, name) FROM stdin;
\.


--
-- Name: access_emailalias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_emailalias_id_seq', 1, false);


--
-- Name: access_emailaliasdomain_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_emailaliasdomain_id_seq', 1, false);


--
-- Name: access_emailaliastype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_emailaliastype_id_seq', 1, false);


--
-- Name: access_grantedprivilege_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_grantedprivilege_id_seq', 1, false);


--
-- Name: access_groupemailaliasgrant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_groupemailaliasgrant_id_seq', 1, false);


--
-- Name: access_groupprivilege_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_groupprivilege_id_seq', 1, false);


--
-- Name: access_internalemailalias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_internalemailalias_id_seq', 1, false);


--
-- Name: access_privilege_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_privilege_id_seq', 1, false);


--
-- Name: access_slackaccess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_slackaccess_id_seq', 1, false);


--
-- Name: access_smtppassword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_smtppassword_id_seq', 1, false);


--
-- Name: access_smtpserver_domains_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_smtpserver_domains_id_seq', 1, false);


--
-- Name: access_smtpserver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.access_smtpserver_id_seq', 1, false);


--
-- Name: aicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.aicon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: aicon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.aicon2016_specialdiet_id_seq', 1, false);


--
-- Name: aicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.aicon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: aicon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.aicon2018_specialdiet_id_seq', 1, false);


--
-- Name: animecon2015_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2015_night_id_seq', 1, false);


--
-- Name: animecon2015_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2015_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: animecon2015_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2015_signupextra_special_diet_id_seq', 1, false);


--
-- Name: animecon2015_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2015_specialdiet_id_seq', 1, false);


--
-- Name: animecon2016_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2016_night_id_seq', 1, false);


--
-- Name: animecon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2016_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: animecon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: animecon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.animecon2016_specialdiet_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 684, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, false);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: badges_badge_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.badges_badge_id_seq', 1, false);


--
-- Name: badges_batch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.badges_batch_id_seq', 1, false);


--
-- Name: core_carouselslide_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_carouselslide_id_seq', 1, false);


--
-- Name: core_emailverificationtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_emailverificationtoken_id_seq', 1, false);


--
-- Name: core_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_event_id_seq', 1, false);


--
-- Name: core_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_organization_id_seq', 1, false);


--
-- Name: core_passwordresettoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_passwordresettoken_id_seq', 1, false);


--
-- Name: core_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_person_id_seq', 1, false);


--
-- Name: core_venue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.core_venue_id_seq', 1, false);


--
-- Name: desucon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: desucon2016_signupextrav2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2016_signupextrav2_id_seq', 1, false);


--
-- Name: desucon2016_signupextrav2_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2016_signupextrav2_special_diet_id_seq', 1, false);


--
-- Name: desucon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2016_specialdiet_id_seq', 1, false);


--
-- Name: desucon2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2017_signupextra_id_seq', 1, false);


--
-- Name: desucon2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: desucon2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2017_specialdiet_id_seq', 1, false);


--
-- Name: desucon2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2018_signupextra_id_seq', 1, false);


--
-- Name: desucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: desucon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2018_specialdiet_id_seq', 1, false);


--
-- Name: desucon2019_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2019_signupextra_id_seq', 1, false);


--
-- Name: desucon2019_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2019_signupextra_special_diet_id_seq', 1, false);


--
-- Name: desucon2019_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desucon2019_specialdiet_id_seq', 1, false);


--
-- Name: desuprofile_integration_confirmationcode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.desuprofile_integration_confirmationcode_id_seq', 1, false);


--
-- Name: directory_directoryaccessgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.directory_directoryaccessgroup_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 228, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 439, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: enrollment_conconpart_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_conconpart_id_seq', 1, false);


--
-- Name: enrollment_enrollment_concon_parts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_enrollment_concon_parts_id_seq', 1, false);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 1, false);


--
-- Name: enrollment_enrollment_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_enrollment_special_diet_id_seq', 1, false);


--
-- Name: enrollment_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.enrollment_specialdiet_id_seq', 1, false);


--
-- Name: event_log_entry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.event_log_entry_id_seq', 1, false);


--
-- Name: event_log_subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.event_log_subscription_id_seq', 1, false);


--
-- Name: feedback_feedbackmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.feedback_feedbackmessage_id_seq', 1, false);


--
-- Name: finncon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.finncon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: finncon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.finncon2016_specialdiet_id_seq', 1, false);


--
-- Name: finncon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.finncon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: finncon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.finncon2018_specialdiet_id_seq', 1, false);


--
-- Name: frostbite2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2017_signupextra_id_seq', 1, false);


--
-- Name: frostbite2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: frostbite2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2017_specialdiet_id_seq', 1, false);


--
-- Name: frostbite2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2018_signupextra_id_seq', 1, false);


--
-- Name: frostbite2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: frostbite2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2018_specialdiet_id_seq', 1, false);


--
-- Name: frostbite2019_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2019_signupextra_id_seq', 1, false);


--
-- Name: frostbite2019_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2019_signupextra_special_diet_id_seq', 1, false);


--
-- Name: frostbite2019_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.frostbite2019_specialdiet_id_seq', 1, false);


--
-- Name: hitpoint2015_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hitpoint2015_signupextra_special_diet_id_seq', 1, false);


--
-- Name: hitpoint2015_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hitpoint2015_specialdiet_id_seq', 1, false);


--
-- Name: hitpoint2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hitpoint2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: hitpoint2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hitpoint2017_specialdiet_id_seq', 1, false);


--
-- Name: hitpoint2017_timeslot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hitpoint2017_timeslot_id_seq', 1, false);


--
-- Name: intra_team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.intra_team_id_seq', 1, false);


--
-- Name: intra_teammember_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.intra_teammember_id_seq', 1, false);


--
-- Name: kawacon2016_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2016_night_id_seq', 1, false);


--
-- Name: kawacon2016_signupextra_needs_lodging_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2016_signupextra_needs_lodging_id_seq', 1, false);


--
-- Name: kawacon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kawacon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2016_specialdiet_id_seq', 1, false);


--
-- Name: kawacon2017_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_night_id_seq', 1, false);


--
-- Name: kawacon2017_shift_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_shift_id_seq', 1, false);


--
-- Name: kawacon2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_signupextra_id_seq', 1, false);


--
-- Name: kawacon2017_signupextra_needs_lodging_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_signupextra_needs_lodging_id_seq', 1, false);


--
-- Name: kawacon2017_signupextra_shifts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_signupextra_shifts_id_seq', 1, false);


--
-- Name: kawacon2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kawacon2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kawacon2017_specialdiet_id_seq', 1, false);


--
-- Name: kuplii2015_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2015_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kuplii2015_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2015_specialdiet_id_seq', 1, false);


--
-- Name: kuplii2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kuplii2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2016_specialdiet_id_seq', 1, false);


--
-- Name: kuplii2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2017_signupextra_id_seq', 1, false);


--
-- Name: kuplii2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kuplii2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2017_specialdiet_id_seq', 1, false);


--
-- Name: kuplii2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2018_signupextra_id_seq', 1, false);


--
-- Name: kuplii2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: kuplii2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.kuplii2018_specialdiet_id_seq', 1, false);


--
-- Name: labour_alternativesignupform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_alternativesignupform_id_seq', 1, false);


--
-- Name: labour_emptysignupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_emptysignupextra_id_seq', 1, false);


--
-- Name: labour_infolink_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_infolink_id_seq', 1, false);


--
-- Name: labour_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_job_id_seq', 1, false);


--
-- Name: labour_jobcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_jobcategory_id_seq', 1, false);


--
-- Name: labour_jobcategory_personnel_classes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_jobcategory_personnel_classes_id_seq', 1, false);


--
-- Name: labour_jobcategory_required_qualifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_jobcategory_required_qualifications_id_seq', 1, false);


--
-- Name: labour_jobrequirement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_jobrequirement_id_seq', 1, false);


--
-- Name: labour_perk_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_perk_id_seq', 1, false);


--
-- Name: labour_personnelclass_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_personnelclass_id_seq', 1, false);


--
-- Name: labour_personnelclass_perks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_personnelclass_perks_id_seq', 1, false);


--
-- Name: labour_personqualification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_personqualification_id_seq', 1, false);


--
-- Name: labour_qualification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_qualification_id_seq', 1, false);


--
-- Name: labour_shift_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_shift_id_seq', 1, false);


--
-- Name: labour_signup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_signup_id_seq', 1, false);


--
-- Name: labour_signup_job_categories_accepted_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_signup_job_categories_accepted_id_seq', 1, false);


--
-- Name: labour_signup_job_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_signup_job_categories_id_seq', 1, false);


--
-- Name: labour_signup_job_categories_rejected_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_signup_job_categories_rejected_id_seq', 1, false);


--
-- Name: labour_signup_personnel_classes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_signup_personnel_classes_id_seq', 1, false);


--
-- Name: labour_survey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_survey_id_seq', 1, false);


--
-- Name: labour_surveyrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_surveyrecord_id_seq', 1, false);


--
-- Name: labour_workperiod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.labour_workperiod_id_seq', 1, false);


--
-- Name: lakeuscon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lakeuscon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: lakeuscon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lakeuscon2016_specialdiet_id_seq', 1, false);


--
-- Name: lippukala_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lippukala_code_id_seq', 1, false);


--
-- Name: lippukala_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.lippukala_order_id_seq', 1, false);


--
-- Name: listings_externalevent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.listings_externalevent_id_seq', 1, false);


--
-- Name: listings_listing_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.listings_listing_events_id_seq', 1, false);


--
-- Name: listings_listing_external_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.listings_listing_external_events_id_seq', 1, false);


--
-- Name: listings_listing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.listings_listing_id_seq', 1, false);


--
-- Name: mailings_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mailings_message_id_seq', 1, false);


--
-- Name: mailings_personmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mailings_personmessage_id_seq', 1, false);


--
-- Name: mailings_personmessagebody_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mailings_personmessagebody_id_seq', 1, false);


--
-- Name: mailings_personmessagesubject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mailings_personmessagesubject_id_seq', 1, false);


--
-- Name: mailings_recipientgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mailings_recipientgroup_id_seq', 1, false);


--
-- Name: matsucon2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matsucon2018_signupextra_id_seq', 1, false);


--
-- Name: matsucon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.matsucon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: membership_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.membership_membership_id_seq', 1, false);


--
-- Name: membership_membershipfeepayment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.membership_membershipfeepayment_id_seq', 1, false);


--
-- Name: membership_term_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.membership_term_id_seq', 1, false);


--
-- Name: mimicon2016_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2016_night_id_seq', 1, false);


--
-- Name: mimicon2016_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2016_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: mimicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: mimicon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2016_specialdiet_id_seq', 1, false);


--
-- Name: mimicon2018_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2018_night_id_seq', 1, false);


--
-- Name: mimicon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2018_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: mimicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: mimicon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.mimicon2018_specialdiet_id_seq', 1, false);


--
-- Name: nexmo_deliverystatusfragment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nexmo_deliverystatusfragment_id_seq', 1, false);


--
-- Name: nexmo_inboundmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nexmo_inboundmessage_id_seq', 1, false);


--
-- Name: nexmo_inboundmessagefragment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nexmo_inboundmessagefragment_id_seq', 1, false);


--
-- Name: nexmo_outboundmessage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nexmo_outboundmessage_id_seq', 1, false);


--
-- Name: nippori2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.nippori2017_signupextra_id_seq', 1, false);


--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.oauth2_provider_accesstoken_id_seq', 1, false);


--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.oauth2_provider_application_id_seq', 1, false);


--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.oauth2_provider_grant_id_seq', 1, false);


--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.oauth2_provider_refreshtoken_id_seq', 1, false);


--
-- Name: payments_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.payments_payment_id_seq', 1, false);


--
-- Name: popcult2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.popcult2017_signupextra_id_seq', 1, false);


--
-- Name: popcult2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.popcult2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: popcultday2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.popcultday2018_signupextra_id_seq', 1, false);


--
-- Name: popcultday2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.popcultday2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: programme_alternativeprogrammeform_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_alternativeprogrammeform_id_seq', 1, false);


--
-- Name: programme_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_category_id_seq', 1, false);


--
-- Name: programme_freeformorganizer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_freeformorganizer_id_seq', 1, false);


--
-- Name: programme_invitation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_invitation_id_seq', 1, false);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programme_hitpoint2017_preferred_time_slots_id_seq', 1, false);


--
-- Name: programme_programme_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programme_id_seq', 1, false);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programme_ropecon2018_preferred_time_slots_id_seq', 1, false);


--
-- Name: programme_programme_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programme_tags_id_seq', 1, false);


--
-- Name: programme_programmefeedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programmefeedback_id_seq', 1, false);


--
-- Name: programme_programmerole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_programmerole_id_seq', 1, false);


--
-- Name: programme_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_role_id_seq', 1, false);


--
-- Name: programme_room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_room_id_seq', 1, false);


--
-- Name: programme_specialstarttime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_specialstarttime_id_seq', 1, false);


--
-- Name: programme_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_tag_id_seq', 1, false);


--
-- Name: programme_timeblock_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_timeblock_id_seq', 1, false);


--
-- Name: programme_view_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_view_id_seq', 1, false);


--
-- Name: programme_viewroom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.programme_viewroom_id_seq', 1, false);


--
-- Name: ropecon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ropecon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: ropecon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ropecon2018_specialdiet_id_seq', 1, false);


--
-- Name: ropecon2018_timeslot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.ropecon2018_timeslot_id_seq', 1, false);


--
-- Name: shippocon2016_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.shippocon2016_signupextra_id_seq', 1, false);


--
-- Name: shippocon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.shippocon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: shippocon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.shippocon2016_specialdiet_id_seq', 1, false);


--
-- Name: sms_hotword_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_hotword_id_seq', 1, false);


--
-- Name: sms_nominee_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_nominee_category_id_seq', 1, false);


--
-- Name: sms_nominee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_nominee_id_seq', 1, false);


--
-- Name: sms_smsmessagein_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_smsmessagein_id_seq', 1, false);


--
-- Name: sms_smsmessageout_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_smsmessageout_id_seq', 1, false);


--
-- Name: sms_vote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_vote_id_seq', 1, false);


--
-- Name: sms_votecategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sms_votecategory_id_seq', 1, false);


--
-- Name: surveys_eventsurvey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.surveys_eventsurvey_id_seq', 1, false);


--
-- Name: surveys_eventsurveyresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.surveys_eventsurveyresult_id_seq', 1, false);


--
-- Name: surveys_globalsurvey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.surveys_globalsurvey_id_seq', 1, false);


--
-- Name: surveys_globalsurveyresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.surveys_globalsurveyresult_id_seq', 1, false);


--
-- Name: tickets_accommodationinformation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_accommodationinformation_id_seq', 1, false);


--
-- Name: tickets_accommodationinformation_limit_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_accommodationinformation_limit_groups_id_seq', 1, false);


--
-- Name: tickets_batch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_batch_id_seq', 1, false);


--
-- Name: tickets_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_customer_id_seq', 1, false);


--
-- Name: tickets_limitgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_limitgroup_id_seq', 1, false);


--
-- Name: tickets_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_order_id_seq', 1, false);


--
-- Name: tickets_orderproduct_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_orderproduct_id_seq', 1, false);


--
-- Name: tickets_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_product_id_seq', 1, false);


--
-- Name: tickets_product_limit_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_product_limit_groups_id_seq', 1, false);


--
-- Name: tickets_shirtorder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_shirtorder_id_seq', 1, false);


--
-- Name: tickets_shirtsize_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_shirtsize_id_seq', 1, false);


--
-- Name: tickets_shirttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tickets_shirttype_id_seq', 1, false);


--
-- Name: tracon11_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_night_id_seq', 1, false);


--
-- Name: tracon11_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: tracon11_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_signupextra_special_diet_id_seq', 1, false);


--
-- Name: tracon11_signupextrav2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_signupextrav2_id_seq', 1, false);


--
-- Name: tracon11_signupextrav2_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_signupextrav2_lodging_needs_id_seq', 1, false);


--
-- Name: tracon11_signupextrav2_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_signupextrav2_special_diet_id_seq', 1, false);


--
-- Name: tracon11_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon11_specialdiet_id_seq', 1, false);


--
-- Name: tracon2017_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_night_id_seq', 1, false);


--
-- Name: tracon2017_poison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_poison_id_seq', 1, false);


--
-- Name: tracon2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_signupextra_id_seq', 1, false);


--
-- Name: tracon2017_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: tracon2017_signupextra_pick_your_poison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_signupextra_pick_your_poison_id_seq', 1, false);


--
-- Name: tracon2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: tracon2018_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_night_id_seq', 1, false);


--
-- Name: tracon2018_poison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_poison_id_seq', 1, false);


--
-- Name: tracon2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_signupextra_id_seq', 1, false);


--
-- Name: tracon2018_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: tracon2018_signupextra_pick_your_poison_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_signupextra_pick_your_poison_id_seq', 1, false);


--
-- Name: tracon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: tracon9_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon9_night_id_seq', 1, false);


--
-- Name: tracon9_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon9_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: tracon9_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon9_signupextra_special_diet_id_seq', 1, false);


--
-- Name: tracon9_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracon9_specialdiet_id_seq', 1, false);


--
-- Name: traconx_night_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.traconx_night_id_seq', 1, false);


--
-- Name: traconx_signupextra_lodging_needs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.traconx_signupextra_lodging_needs_id_seq', 1, false);


--
-- Name: traconx_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.traconx_signupextra_special_diet_id_seq', 1, false);


--
-- Name: traconx_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.traconx_specialdiet_id_seq', 1, false);


--
-- Name: tylycon2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tylycon2017_signupextra_id_seq', 1, false);


--
-- Name: tylycon2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tylycon2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: tylycon2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tylycon2017_specialdiet_id_seq', 1, false);


--
-- Name: worldcon75_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.worldcon75_signupextra_id_seq', 1, false);


--
-- Name: worldcon75_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.worldcon75_signupextra_special_diet_id_seq', 1, false);


--
-- Name: yukicon2016_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2016_signupextra_special_diet_id_seq', 1, false);


--
-- Name: yukicon2016_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2016_specialdiet_id_seq', 1, false);


--
-- Name: yukicon2017_eventday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2017_eventday_id_seq', 1, false);


--
-- Name: yukicon2017_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2017_signupextra_id_seq', 1, false);


--
-- Name: yukicon2017_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2017_signupextra_special_diet_id_seq', 1, false);


--
-- Name: yukicon2017_signupextra_work_days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2017_signupextra_work_days_id_seq', 1, false);


--
-- Name: yukicon2017_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2017_specialdiet_id_seq', 1, false);


--
-- Name: yukicon2018_eventday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2018_eventday_id_seq', 1, false);


--
-- Name: yukicon2018_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2018_signupextra_id_seq', 1, false);


--
-- Name: yukicon2018_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2018_signupextra_special_diet_id_seq', 1, false);


--
-- Name: yukicon2018_signupextra_work_days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2018_signupextra_work_days_id_seq', 1, false);


--
-- Name: yukicon2018_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2018_specialdiet_id_seq', 1, false);


--
-- Name: yukicon2019_eventday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2019_eventday_id_seq', 1, false);


--
-- Name: yukicon2019_signupextra_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2019_signupextra_id_seq', 1, false);


--
-- Name: yukicon2019_signupextra_special_diet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2019_signupextra_special_diet_id_seq', 1, false);


--
-- Name: yukicon2019_signupextra_work_days_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2019_signupextra_work_days_id_seq', 1, false);


--
-- Name: yukicon2019_specialdiet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yukicon2019_specialdiet_id_seq', 1, false);


--
-- Name: access_accessorganizationmeta access_accessorganizationmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_accessorganizationmeta
    ADD CONSTRAINT access_accessorganizationmeta_pkey PRIMARY KEY (organization_id);


--
-- Name: access_emailalias access_emailalias_domain_id_4f0f253c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT access_emailalias_domain_id_4f0f253c_uniq UNIQUE (domain_id, account_name);


--
-- Name: access_emailalias access_emailalias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT access_emailalias_pkey PRIMARY KEY (id);


--
-- Name: access_emailaliasdomain access_emailaliasdomain_domain_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliasdomain
    ADD CONSTRAINT access_emailaliasdomain_domain_name_key UNIQUE (domain_name);


--
-- Name: access_emailaliasdomain access_emailaliasdomain_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliasdomain
    ADD CONSTRAINT access_emailaliasdomain_pkey PRIMARY KEY (id);


--
-- Name: access_emailaliastype access_emailaliastype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliastype
    ADD CONSTRAINT access_emailaliastype_pkey PRIMARY KEY (id);


--
-- Name: access_grantedprivilege access_grantedprivilege_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_grantedprivilege
    ADD CONSTRAINT access_grantedprivilege_pkey PRIMARY KEY (id);


--
-- Name: access_grantedprivilege access_grantedprivilege_privilege_id_e3794977_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_grantedprivilege
    ADD CONSTRAINT access_grantedprivilege_privilege_id_e3794977_uniq UNIQUE (privilege_id, person_id);


--
-- Name: access_groupemailaliasgrant access_groupemailaliasgrant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupemailaliasgrant
    ADD CONSTRAINT access_groupemailaliasgrant_pkey PRIMARY KEY (id);


--
-- Name: access_groupprivilege access_groupprivilege_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege
    ADD CONSTRAINT access_groupprivilege_pkey PRIMARY KEY (id);


--
-- Name: access_groupprivilege access_groupprivilege_privilege_id_a358dca1_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege
    ADD CONSTRAINT access_groupprivilege_privilege_id_a358dca1_uniq UNIQUE (privilege_id, group_id);


--
-- Name: access_internalemailalias access_internalemailalias_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_internalemailalias
    ADD CONSTRAINT access_internalemailalias_pkey PRIMARY KEY (id);


--
-- Name: access_privilege access_privilege_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_privilege
    ADD CONSTRAINT access_privilege_pkey PRIMARY KEY (id);


--
-- Name: access_privilege access_privilege_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_privilege
    ADD CONSTRAINT access_privilege_slug_key UNIQUE (slug);


--
-- Name: access_slackaccess access_slackaccess_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_slackaccess
    ADD CONSTRAINT access_slackaccess_pkey PRIMARY KEY (id);


--
-- Name: access_slackaccess access_slackaccess_privilege_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_slackaccess
    ADD CONSTRAINT access_slackaccess_privilege_id_key UNIQUE (privilege_id);


--
-- Name: access_smtppassword access_smtppassword_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtppassword
    ADD CONSTRAINT access_smtppassword_pkey PRIMARY KEY (id);


--
-- Name: access_smtpserver_domains access_smtpserver_domains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver_domains
    ADD CONSTRAINT access_smtpserver_domains_pkey PRIMARY KEY (id);


--
-- Name: access_smtpserver_domains access_smtpserver_domains_smtpserver_id_4cdb5485_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver_domains
    ADD CONSTRAINT access_smtpserver_domains_smtpserver_id_4cdb5485_uniq UNIQUE (smtpserver_id, emailaliasdomain_id);


--
-- Name: access_smtpserver access_smtpserver_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver
    ADD CONSTRAINT access_smtpserver_pkey PRIMARY KEY (id);


--
-- Name: aicon2016_signupextra aicon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra
    ADD CONSTRAINT aicon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: aicon2016_signupextra_special_diet aicon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra_special_diet
    ADD CONSTRAINT aicon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: aicon2016_signupextra_special_diet aicon2016_signupextra_special_diet_signupextra_id_6e96611f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra_special_diet
    ADD CONSTRAINT aicon2016_signupextra_special_diet_signupextra_id_6e96611f_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: aicon2016_specialdiet aicon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_specialdiet
    ADD CONSTRAINT aicon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: aicon2018_signupextra aicon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra
    ADD CONSTRAINT aicon2018_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: aicon2018_signupextra_special_diet aicon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra_special_diet
    ADD CONSTRAINT aicon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: aicon2018_signupextra_special_diet aicon2018_signupextra_special_diet_signupextra_id_74e0ff39_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra_special_diet
    ADD CONSTRAINT aicon2018_signupextra_special_diet_signupextra_id_74e0ff39_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: aicon2018_specialdiet aicon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_specialdiet
    ADD CONSTRAINT aicon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: animecon2015_night animecon2015_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_night
    ADD CONSTRAINT animecon2015_night_pkey PRIMARY KEY (id);


--
-- Name: animecon2015_signupextra_lodging_needs animecon2015_signupextra_lodging_n_signupextra_id_e0eb73d2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_lodging_needs
    ADD CONSTRAINT animecon2015_signupextra_lodging_n_signupextra_id_e0eb73d2_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: animecon2015_signupextra_lodging_needs animecon2015_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_lodging_needs
    ADD CONSTRAINT animecon2015_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: animecon2015_signupextra animecon2015_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra
    ADD CONSTRAINT animecon2015_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: animecon2015_signupextra_special_diet animecon2015_signupextra_special_d_signupextra_id_54d8fa93_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_special_diet
    ADD CONSTRAINT animecon2015_signupextra_special_d_signupextra_id_54d8fa93_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: animecon2015_signupextra_special_diet animecon2015_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_special_diet
    ADD CONSTRAINT animecon2015_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: animecon2015_specialdiet animecon2015_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_specialdiet
    ADD CONSTRAINT animecon2015_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: animecon2016_night animecon2016_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_night
    ADD CONSTRAINT animecon2016_night_pkey PRIMARY KEY (id);


--
-- Name: animecon2016_signupextra_lodging_needs animecon2016_signupextra_lodging_n_signupextra_id_33b9ec19_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_lodging_needs
    ADD CONSTRAINT animecon2016_signupextra_lodging_n_signupextra_id_33b9ec19_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: animecon2016_signupextra_lodging_needs animecon2016_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_lodging_needs
    ADD CONSTRAINT animecon2016_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: animecon2016_signupextra animecon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra
    ADD CONSTRAINT animecon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: animecon2016_signupextra_special_diet animecon2016_signupextra_special_d_signupextra_id_9027b824_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_special_diet
    ADD CONSTRAINT animecon2016_signupextra_special_d_signupextra_id_9027b824_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: animecon2016_signupextra_special_diet animecon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_special_diet
    ADD CONSTRAINT animecon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: animecon2016_specialdiet animecon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_specialdiet
    ADD CONSTRAINT animecon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: badges_badge badges_badge_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges_badge_pkey PRIMARY KEY (id);


--
-- Name: badges_badgeseventmeta badges_badgeseventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badgeseventmeta
    ADD CONSTRAINT badges_badgeseventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: badges_batch badges_batch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_batch
    ADD CONSTRAINT badges_batch_pkey PRIMARY KEY (id);


--
-- Name: core_carouselslide core_carouselslide_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_carouselslide
    ADD CONSTRAINT core_carouselslide_pkey PRIMARY KEY (id);


--
-- Name: core_emailverificationtoken core_emailverificationtoken_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_emailverificationtoken
    ADD CONSTRAINT core_emailverificationtoken_code_key UNIQUE (code);


--
-- Name: core_emailverificationtoken core_emailverificationtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_emailverificationtoken
    ADD CONSTRAINT core_emailverificationtoken_pkey PRIMARY KEY (id);


--
-- Name: core_event core_event_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_pkey PRIMARY KEY (id);


--
-- Name: core_event core_event_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_slug_key UNIQUE (slug);


--
-- Name: core_organization core_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_organization
    ADD CONSTRAINT core_organization_pkey PRIMARY KEY (id);


--
-- Name: core_organization core_organization_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_organization
    ADD CONSTRAINT core_organization_slug_key UNIQUE (slug);


--
-- Name: core_passwordresettoken core_passwordresettoken_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_passwordresettoken
    ADD CONSTRAINT core_passwordresettoken_code_key UNIQUE (code);


--
-- Name: core_passwordresettoken core_passwordresettoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_passwordresettoken
    ADD CONSTRAINT core_passwordresettoken_pkey PRIMARY KEY (id);


--
-- Name: core_person core_person_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_person
    ADD CONSTRAINT core_person_pkey PRIMARY KEY (id);


--
-- Name: core_person core_person_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_person
    ADD CONSTRAINT core_person_user_id_key UNIQUE (user_id);


--
-- Name: core_venue core_venue_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_venue
    ADD CONSTRAINT core_venue_pkey PRIMARY KEY (id);


--
-- Name: desucon2016_signupextra desucon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra
    ADD CONSTRAINT desucon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: desucon2016_signupextra_special_diet desucon2016_signupextra_special_di_signupextra_id_842872af_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra_special_diet
    ADD CONSTRAINT desucon2016_signupextra_special_di_signupextra_id_842872af_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: desucon2016_signupextra_special_diet desucon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra_special_diet
    ADD CONSTRAINT desucon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: desucon2016_signupextrav2 desucon2016_signupextrav2_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2
    ADD CONSTRAINT desucon2016_signupextrav2_person_id_key UNIQUE (person_id);


--
-- Name: desucon2016_signupextrav2 desucon2016_signupextrav2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2
    ADD CONSTRAINT desucon2016_signupextrav2_pkey PRIMARY KEY (id);


--
-- Name: desucon2016_signupextrav2_special_diet desucon2016_signupextrav2_specia_signupextrav2_id_d3b6b9a3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2_special_diet
    ADD CONSTRAINT desucon2016_signupextrav2_specia_signupextrav2_id_d3b6b9a3_uniq UNIQUE (signupextrav2_id, specialdiet_id);


--
-- Name: desucon2016_signupextrav2_special_diet desucon2016_signupextrav2_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2_special_diet
    ADD CONSTRAINT desucon2016_signupextrav2_special_diet_pkey PRIMARY KEY (id);


--
-- Name: desucon2016_specialdiet desucon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_specialdiet
    ADD CONSTRAINT desucon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: desucon2017_signupextra desucon2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra
    ADD CONSTRAINT desucon2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: desucon2017_signupextra desucon2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra
    ADD CONSTRAINT desucon2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: desucon2017_signupextra_special_diet desucon2017_signupextra_special_di_signupextra_id_5bcb5d88_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra_special_diet
    ADD CONSTRAINT desucon2017_signupextra_special_di_signupextra_id_5bcb5d88_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: desucon2017_signupextra_special_diet desucon2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra_special_diet
    ADD CONSTRAINT desucon2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: desucon2017_specialdiet desucon2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_specialdiet
    ADD CONSTRAINT desucon2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: desucon2018_signupextra desucon2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra
    ADD CONSTRAINT desucon2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: desucon2018_signupextra desucon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra
    ADD CONSTRAINT desucon2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: desucon2018_signupextra_special_diet desucon2018_signupextra_special_di_signupextra_id_9daac4a3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra_special_diet
    ADD CONSTRAINT desucon2018_signupextra_special_di_signupextra_id_9daac4a3_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: desucon2018_signupextra_special_diet desucon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra_special_diet
    ADD CONSTRAINT desucon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: desucon2018_specialdiet desucon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_specialdiet
    ADD CONSTRAINT desucon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: desucon2019_signupextra desucon2019_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra
    ADD CONSTRAINT desucon2019_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: desucon2019_signupextra desucon2019_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra
    ADD CONSTRAINT desucon2019_signupextra_pkey PRIMARY KEY (id);


--
-- Name: desucon2019_signupextra_special_diet desucon2019_signupextra_special_di_signupextra_id_01cb1623_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra_special_diet
    ADD CONSTRAINT desucon2019_signupextra_special_di_signupextra_id_01cb1623_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: desucon2019_signupextra_special_diet desucon2019_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra_special_diet
    ADD CONSTRAINT desucon2019_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: desucon2019_specialdiet desucon2019_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_specialdiet
    ADD CONSTRAINT desucon2019_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: desuprofile_integration_confirmationcode desuprofile_integration_confirmationcode_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_confirmationcode
    ADD CONSTRAINT desuprofile_integration_confirmationcode_code_key UNIQUE (code);


--
-- Name: desuprofile_integration_confirmationcode desuprofile_integration_confirmationcode_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_confirmationcode
    ADD CONSTRAINT desuprofile_integration_confirmationcode_pkey PRIMARY KEY (id);


--
-- Name: desuprofile_integration_connection desuprofile_integration_connection_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_connection
    ADD CONSTRAINT desuprofile_integration_connection_pkey PRIMARY KEY (id);


--
-- Name: desuprofile_integration_connection desuprofile_integration_connection_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_connection
    ADD CONSTRAINT desuprofile_integration_connection_user_id_key UNIQUE (user_id);


--
-- Name: directory_directoryaccessgroup directory_directoryaccessgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryaccessgroup
    ADD CONSTRAINT directory_directoryaccessgroup_pkey PRIMARY KEY (id);


--
-- Name: directory_directoryorganizationmeta directory_directoryorganizationmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryorganizationmeta
    ADD CONSTRAINT directory_directoryorganizationmeta_pkey PRIMARY KEY (organization_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site django_site_domain_a2e37b91_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);


--
-- Name: django_site django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: enrollment_conconpart enrollment_conconpart_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_conconpart
    ADD CONSTRAINT enrollment_conconpart_pkey PRIMARY KEY (id);


--
-- Name: enrollment_enrollment_concon_parts enrollment_enrollment_concon_parts_enrollment_id_b5bba3e3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_concon_parts
    ADD CONSTRAINT enrollment_enrollment_concon_parts_enrollment_id_b5bba3e3_uniq UNIQUE (enrollment_id, conconpart_id);


--
-- Name: enrollment_enrollment_concon_parts enrollment_enrollment_concon_parts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_concon_parts
    ADD CONSTRAINT enrollment_enrollment_concon_parts_pkey PRIMARY KEY (id);


--
-- Name: enrollment_enrollment enrollment_enrollment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment
    ADD CONSTRAINT enrollment_enrollment_pkey PRIMARY KEY (id);


--
-- Name: enrollment_enrollment_special_diet enrollment_enrollment_special_diet_enrollment_id_98ce4073_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_special_diet
    ADD CONSTRAINT enrollment_enrollment_special_diet_enrollment_id_98ce4073_uniq UNIQUE (enrollment_id, specialdiet_id);


--
-- Name: enrollment_enrollment_special_diet enrollment_enrollment_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_special_diet
    ADD CONSTRAINT enrollment_enrollment_special_diet_pkey PRIMARY KEY (id);


--
-- Name: enrollment_enrollmenteventmeta enrollment_enrollmenteventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollmenteventmeta
    ADD CONSTRAINT enrollment_enrollmenteventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: enrollment_specialdiet enrollment_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_specialdiet
    ADD CONSTRAINT enrollment_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: event_log_entry event_log_entry_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT event_log_entry_pkey PRIMARY KEY (id);


--
-- Name: event_log_subscription event_log_subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_subscription
    ADD CONSTRAINT event_log_subscription_pkey PRIMARY KEY (id);


--
-- Name: feedback_feedbackmessage feedback_feedbackmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feedback_feedbackmessage
    ADD CONSTRAINT feedback_feedbackmessage_pkey PRIMARY KEY (id);


--
-- Name: finncon2016_signupextra finncon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra
    ADD CONSTRAINT finncon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: finncon2016_signupextra_special_diet finncon2016_signupextra_special_di_signupextra_id_4bbb9d18_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra_special_diet
    ADD CONSTRAINT finncon2016_signupextra_special_di_signupextra_id_4bbb9d18_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: finncon2016_signupextra_special_diet finncon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra_special_diet
    ADD CONSTRAINT finncon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: finncon2016_specialdiet finncon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_specialdiet
    ADD CONSTRAINT finncon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: finncon2018_signupextra finncon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra
    ADD CONSTRAINT finncon2018_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: finncon2018_signupextra_special_diet finncon2018_signupextra_special_di_signupextra_id_b4a606b2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra_special_diet
    ADD CONSTRAINT finncon2018_signupextra_special_di_signupextra_id_b4a606b2_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: finncon2018_signupextra_special_diet finncon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra_special_diet
    ADD CONSTRAINT finncon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: finncon2018_specialdiet finncon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_specialdiet
    ADD CONSTRAINT finncon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2016_signupextra frostbite2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2016_signupextra
    ADD CONSTRAINT frostbite2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: frostbite2017_signupextra frostbite2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra
    ADD CONSTRAINT frostbite2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: frostbite2017_signupextra frostbite2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra
    ADD CONSTRAINT frostbite2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: frostbite2017_signupextra_special_diet frostbite2017_signupextra_special__signupextra_id_927ca385_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra_special_diet
    ADD CONSTRAINT frostbite2017_signupextra_special__signupextra_id_927ca385_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: frostbite2017_signupextra_special_diet frostbite2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra_special_diet
    ADD CONSTRAINT frostbite2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2017_specialdiet frostbite2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_specialdiet
    ADD CONSTRAINT frostbite2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2018_signupextra frostbite2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra
    ADD CONSTRAINT frostbite2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: frostbite2018_signupextra frostbite2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra
    ADD CONSTRAINT frostbite2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: frostbite2018_signupextra_special_diet frostbite2018_signupextra_special__signupextra_id_d630d487_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra_special_diet
    ADD CONSTRAINT frostbite2018_signupextra_special__signupextra_id_d630d487_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: frostbite2018_signupextra_special_diet frostbite2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra_special_diet
    ADD CONSTRAINT frostbite2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2018_specialdiet frostbite2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_specialdiet
    ADD CONSTRAINT frostbite2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2019_signupextra frostbite2019_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra
    ADD CONSTRAINT frostbite2019_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: frostbite2019_signupextra frostbite2019_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra
    ADD CONSTRAINT frostbite2019_signupextra_pkey PRIMARY KEY (id);


--
-- Name: frostbite2019_signupextra_special_diet frostbite2019_signupextra_special__signupextra_id_60ee0cfb_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra_special_diet
    ADD CONSTRAINT frostbite2019_signupextra_special__signupextra_id_60ee0cfb_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: frostbite2019_signupextra_special_diet frostbite2019_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra_special_diet
    ADD CONSTRAINT frostbite2019_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: frostbite2019_specialdiet frostbite2019_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_specialdiet
    ADD CONSTRAINT frostbite2019_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: hitpoint2015_signupextra hitpoint2015_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra
    ADD CONSTRAINT hitpoint2015_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: hitpoint2015_signupextra_special_diet hitpoint2015_signupextra_special_d_signupextra_id_b33bb725_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra_special_diet
    ADD CONSTRAINT hitpoint2015_signupextra_special_d_signupextra_id_b33bb725_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: hitpoint2015_signupextra_special_diet hitpoint2015_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra_special_diet
    ADD CONSTRAINT hitpoint2015_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: hitpoint2015_specialdiet hitpoint2015_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_specialdiet
    ADD CONSTRAINT hitpoint2015_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: hitpoint2017_signupextra hitpoint2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra
    ADD CONSTRAINT hitpoint2017_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: hitpoint2017_signupextra_special_diet hitpoint2017_signupextra_special_d_signupextra_id_7a8016bf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra_special_diet
    ADD CONSTRAINT hitpoint2017_signupextra_special_d_signupextra_id_7a8016bf_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: hitpoint2017_signupextra_special_diet hitpoint2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra_special_diet
    ADD CONSTRAINT hitpoint2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: hitpoint2017_specialdiet hitpoint2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_specialdiet
    ADD CONSTRAINT hitpoint2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: hitpoint2017_timeslot hitpoint2017_timeslot_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_timeslot
    ADD CONSTRAINT hitpoint2017_timeslot_pkey PRIMARY KEY (id);


--
-- Name: intra_intraeventmeta intra_intraeventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_intraeventmeta
    ADD CONSTRAINT intra_intraeventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: intra_team intra_team_event_id_7bc13649_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_team
    ADD CONSTRAINT intra_team_event_id_7bc13649_uniq UNIQUE (event_id, slug);


--
-- Name: intra_team intra_team_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_team
    ADD CONSTRAINT intra_team_pkey PRIMARY KEY (id);


--
-- Name: intra_teammember intra_teammember_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_teammember
    ADD CONSTRAINT intra_teammember_pkey PRIMARY KEY (id);


--
-- Name: intra_teammember intra_teammember_team_id_ca1895b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_teammember
    ADD CONSTRAINT intra_teammember_team_id_ca1895b0_uniq UNIQUE (team_id, person_id);


--
-- Name: kawacon2016_night kawacon2016_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_night
    ADD CONSTRAINT kawacon2016_night_pkey PRIMARY KEY (id);


--
-- Name: kawacon2016_signupextra_needs_lodging kawacon2016_signupextra_needs_lodg_signupextra_id_80e164ea_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2016_signupextra_needs_lodg_signupextra_id_80e164ea_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: kawacon2016_signupextra_needs_lodging kawacon2016_signupextra_needs_lodging_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2016_signupextra_needs_lodging_pkey PRIMARY KEY (id);


--
-- Name: kawacon2016_signupextra kawacon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra
    ADD CONSTRAINT kawacon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: kawacon2016_signupextra_special_diet kawacon2016_signupextra_special_di_signupextra_id_213277bf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_special_diet
    ADD CONSTRAINT kawacon2016_signupextra_special_di_signupextra_id_213277bf_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kawacon2016_signupextra_special_diet kawacon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_special_diet
    ADD CONSTRAINT kawacon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kawacon2016_specialdiet kawacon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_specialdiet
    ADD CONSTRAINT kawacon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_night kawacon2017_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_night
    ADD CONSTRAINT kawacon2017_night_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_shift kawacon2017_shift_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_shift
    ADD CONSTRAINT kawacon2017_shift_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_signupextra_needs_lodging kawacon2017_signupextra_needs_lodg_signupextra_id_cf2bc3ad_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2017_signupextra_needs_lodg_signupextra_id_cf2bc3ad_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: kawacon2017_signupextra_needs_lodging kawacon2017_signupextra_needs_lodging_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2017_signupextra_needs_lodging_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_signupextra kawacon2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra
    ADD CONSTRAINT kawacon2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: kawacon2017_signupextra kawacon2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra
    ADD CONSTRAINT kawacon2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_signupextra_shifts kawacon2017_signupextra_shifts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_shifts
    ADD CONSTRAINT kawacon2017_signupextra_shifts_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_signupextra_shifts kawacon2017_signupextra_shifts_signupextra_id_33dcfeda_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_shifts
    ADD CONSTRAINT kawacon2017_signupextra_shifts_signupextra_id_33dcfeda_uniq UNIQUE (signupextra_id, shift_id);


--
-- Name: kawacon2017_signupextra_special_diet kawacon2017_signupextra_special_di_signupextra_id_fbbe89a4_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_special_diet
    ADD CONSTRAINT kawacon2017_signupextra_special_di_signupextra_id_fbbe89a4_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kawacon2017_signupextra_special_diet kawacon2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_special_diet
    ADD CONSTRAINT kawacon2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kawacon2017_specialdiet kawacon2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_specialdiet
    ADD CONSTRAINT kawacon2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2015_signupextra kuplii2015_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra
    ADD CONSTRAINT kuplii2015_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: kuplii2015_signupextra_special_diet kuplii2015_signupextra_special_die_signupextra_id_5878c7df_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra_special_diet
    ADD CONSTRAINT kuplii2015_signupextra_special_die_signupextra_id_5878c7df_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kuplii2015_signupextra_special_diet kuplii2015_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra_special_diet
    ADD CONSTRAINT kuplii2015_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2015_specialdiet kuplii2015_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_specialdiet
    ADD CONSTRAINT kuplii2015_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2016_signupextra kuplii2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra
    ADD CONSTRAINT kuplii2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: kuplii2016_signupextra_special_diet kuplii2016_signupextra_special_die_signupextra_id_da403e78_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra_special_diet
    ADD CONSTRAINT kuplii2016_signupextra_special_die_signupextra_id_da403e78_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kuplii2016_signupextra_special_diet kuplii2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra_special_diet
    ADD CONSTRAINT kuplii2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2016_specialdiet kuplii2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_specialdiet
    ADD CONSTRAINT kuplii2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2017_signupextra kuplii2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra
    ADD CONSTRAINT kuplii2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: kuplii2017_signupextra kuplii2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra
    ADD CONSTRAINT kuplii2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: kuplii2017_signupextra_special_diet kuplii2017_signupextra_special_die_signupextra_id_5bf1a963_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra_special_diet
    ADD CONSTRAINT kuplii2017_signupextra_special_die_signupextra_id_5bf1a963_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kuplii2017_signupextra_special_diet kuplii2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra_special_diet
    ADD CONSTRAINT kuplii2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2017_specialdiet kuplii2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_specialdiet
    ADD CONSTRAINT kuplii2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2018_signupextra kuplii2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra
    ADD CONSTRAINT kuplii2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: kuplii2018_signupextra kuplii2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra
    ADD CONSTRAINT kuplii2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: kuplii2018_signupextra_special_diet kuplii2018_signupextra_special_die_signupextra_id_dc1c3364_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra_special_diet
    ADD CONSTRAINT kuplii2018_signupextra_special_die_signupextra_id_dc1c3364_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: kuplii2018_signupextra_special_diet kuplii2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra_special_diet
    ADD CONSTRAINT kuplii2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: kuplii2018_specialdiet kuplii2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_specialdiet
    ADD CONSTRAINT kuplii2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: labour_alternativesignupform labour_alternativesignupform_event_id_6c915f19_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_alternativesignupform
    ADD CONSTRAINT labour_alternativesignupform_event_id_6c915f19_uniq UNIQUE (event_id, slug);


--
-- Name: labour_alternativesignupform labour_alternativesignupform_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_alternativesignupform
    ADD CONSTRAINT labour_alternativesignupform_pkey PRIMARY KEY (id);


--
-- Name: labour_common_qualifications_jvkortti labour_common_qualifications_jvkortti_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_common_qualifications_jvkortti
    ADD CONSTRAINT labour_common_qualifications_jvkortti_pkey PRIMARY KEY (personqualification_id);


--
-- Name: labour_emptysignupextra labour_emptysignupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_emptysignupextra
    ADD CONSTRAINT labour_emptysignupextra_person_id_key UNIQUE (person_id);


--
-- Name: labour_obsoleteemptysignupextrav1 labour_emptysignupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_obsoleteemptysignupextrav1
    ADD CONSTRAINT labour_emptysignupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: labour_emptysignupextra labour_emptysignupextra_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_emptysignupextra
    ADD CONSTRAINT labour_emptysignupextra_pkey1 PRIMARY KEY (id);


--
-- Name: labour_infolink labour_infolink_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_infolink
    ADD CONSTRAINT labour_infolink_pkey PRIMARY KEY (id);


--
-- Name: labour_job labour_job_job_category_id_f661b3f2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_job
    ADD CONSTRAINT labour_job_job_category_id_f661b3f2_uniq UNIQUE (job_category_id, slug);


--
-- Name: labour_job labour_job_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_job
    ADD CONSTRAINT labour_job_pkey PRIMARY KEY (id);


--
-- Name: labour_jobcategory labour_jobcategory_event_id_ffdb2b12_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory
    ADD CONSTRAINT labour_jobcategory_event_id_ffdb2b12_uniq UNIQUE (event_id, slug);


--
-- Name: labour_jobcategory_personnel_classes labour_jobcategory_personnel_class_jobcategory_id_3008787b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_personnel_classes
    ADD CONSTRAINT labour_jobcategory_personnel_class_jobcategory_id_3008787b_uniq UNIQUE (jobcategory_id, personnelclass_id);


--
-- Name: labour_jobcategory_personnel_classes labour_jobcategory_personnel_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_personnel_classes
    ADD CONSTRAINT labour_jobcategory_personnel_classes_pkey PRIMARY KEY (id);


--
-- Name: labour_jobcategory labour_jobcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory
    ADD CONSTRAINT labour_jobcategory_pkey PRIMARY KEY (id);


--
-- Name: labour_jobcategory_required_qualifications labour_jobcategory_required_qualif_jobcategory_id_711e457d_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_required_qualifications
    ADD CONSTRAINT labour_jobcategory_required_qualif_jobcategory_id_711e457d_uniq UNIQUE (jobcategory_id, qualification_id);


--
-- Name: labour_jobcategory_required_qualifications labour_jobcategory_required_qualifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_required_qualifications
    ADD CONSTRAINT labour_jobcategory_required_qualifications_pkey PRIMARY KEY (id);


--
-- Name: labour_jobrequirement labour_jobrequirement_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobrequirement
    ADD CONSTRAINT labour_jobrequirement_pkey PRIMARY KEY (id);


--
-- Name: labour_laboureventmeta labour_laboureventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_laboureventmeta
    ADD CONSTRAINT labour_laboureventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: labour_perk labour_perk_event_id_ecc104ea_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_perk
    ADD CONSTRAINT labour_perk_event_id_ecc104ea_uniq UNIQUE (event_id, slug);


--
-- Name: labour_perk labour_perk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_perk
    ADD CONSTRAINT labour_perk_pkey PRIMARY KEY (id);


--
-- Name: labour_personnelclass labour_personnelclass_event_id_1aa04b0b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass
    ADD CONSTRAINT labour_personnelclass_event_id_1aa04b0b_uniq UNIQUE (event_id, slug);


--
-- Name: labour_personnelclass_perks labour_personnelclass_perks_personnelclass_id_521ea9fb_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass_perks
    ADD CONSTRAINT labour_personnelclass_perks_personnelclass_id_521ea9fb_uniq UNIQUE (personnelclass_id, perk_id);


--
-- Name: labour_personnelclass_perks labour_personnelclass_perks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass_perks
    ADD CONSTRAINT labour_personnelclass_perks_pkey PRIMARY KEY (id);


--
-- Name: labour_personnelclass labour_personnelclass_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass
    ADD CONSTRAINT labour_personnelclass_pkey PRIMARY KEY (id);


--
-- Name: labour_personqualification labour_personqualification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personqualification
    ADD CONSTRAINT labour_personqualification_pkey PRIMARY KEY (id);


--
-- Name: labour_qualification labour_qualification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_qualification
    ADD CONSTRAINT labour_qualification_pkey PRIMARY KEY (id);


--
-- Name: labour_qualification labour_qualification_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_qualification
    ADD CONSTRAINT labour_qualification_slug_key UNIQUE (slug);


--
-- Name: labour_shift labour_shift_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_shift
    ADD CONSTRAINT labour_shift_pkey PRIMARY KEY (id);


--
-- Name: labour_signup_job_categories_accepted labour_signup_job_categories_accepted_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_accepted
    ADD CONSTRAINT labour_signup_job_categories_accepted_pkey PRIMARY KEY (id);


--
-- Name: labour_signup_job_categories_accepted labour_signup_job_categories_accepted_signup_id_f0504073_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_accepted
    ADD CONSTRAINT labour_signup_job_categories_accepted_signup_id_f0504073_uniq UNIQUE (signup_id, jobcategory_id);


--
-- Name: labour_signup_job_categories labour_signup_job_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories
    ADD CONSTRAINT labour_signup_job_categories_pkey PRIMARY KEY (id);


--
-- Name: labour_signup_job_categories_rejected labour_signup_job_categories_rejected_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_rejected
    ADD CONSTRAINT labour_signup_job_categories_rejected_pkey PRIMARY KEY (id);


--
-- Name: labour_signup_job_categories_rejected labour_signup_job_categories_rejected_signup_id_ad4784a7_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_rejected
    ADD CONSTRAINT labour_signup_job_categories_rejected_signup_id_ad4784a7_uniq UNIQUE (signup_id, jobcategory_id);


--
-- Name: labour_signup_job_categories labour_signup_job_categories_signup_id_82cace39_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories
    ADD CONSTRAINT labour_signup_job_categories_signup_id_82cace39_uniq UNIQUE (signup_id, jobcategory_id);


--
-- Name: labour_signup_personnel_classes labour_signup_personnel_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_personnel_classes
    ADD CONSTRAINT labour_signup_personnel_classes_pkey PRIMARY KEY (id);


--
-- Name: labour_signup_personnel_classes labour_signup_personnel_classes_signup_id_010f7b9c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_personnel_classes
    ADD CONSTRAINT labour_signup_personnel_classes_signup_id_010f7b9c_uniq UNIQUE (signup_id, personnelclass_id);


--
-- Name: labour_signup labour_signup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup
    ADD CONSTRAINT labour_signup_pkey PRIMARY KEY (id);


--
-- Name: labour_survey labour_survey_event_id_91dd68bd_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_survey
    ADD CONSTRAINT labour_survey_event_id_91dd68bd_uniq UNIQUE (event_id, slug);


--
-- Name: labour_survey labour_survey_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_survey
    ADD CONSTRAINT labour_survey_pkey PRIMARY KEY (id);


--
-- Name: labour_surveyrecord labour_surveyrecord_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_surveyrecord
    ADD CONSTRAINT labour_surveyrecord_pkey PRIMARY KEY (id);


--
-- Name: labour_workperiod labour_workperiod_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_workperiod
    ADD CONSTRAINT labour_workperiod_pkey PRIMARY KEY (id);


--
-- Name: lakeuscon2016_signupextra lakeuscon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra
    ADD CONSTRAINT lakeuscon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: lakeuscon2016_signupextra_special_diet lakeuscon2016_signupextra_special__signupextra_id_d9c8fb0a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra_special_diet
    ADD CONSTRAINT lakeuscon2016_signupextra_special__signupextra_id_d9c8fb0a_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: lakeuscon2016_signupextra_special_diet lakeuscon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra_special_diet
    ADD CONSTRAINT lakeuscon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: lakeuscon2016_specialdiet lakeuscon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_specialdiet
    ADD CONSTRAINT lakeuscon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: lippukala_code lippukala_code_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_code
    ADD CONSTRAINT lippukala_code_code_key UNIQUE (code);


--
-- Name: lippukala_code lippukala_code_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_code
    ADD CONSTRAINT lippukala_code_pkey PRIMARY KEY (id);


--
-- Name: lippukala_order lippukala_order_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_order
    ADD CONSTRAINT lippukala_order_pkey PRIMARY KEY (id);


--
-- Name: lippukala_order lippukala_order_reference_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_order
    ADD CONSTRAINT lippukala_order_reference_number_key UNIQUE (reference_number);


--
-- Name: listings_externalevent listings_externalevent_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_externalevent
    ADD CONSTRAINT listings_externalevent_pkey PRIMARY KEY (id);


--
-- Name: listings_externalevent listings_externalevent_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_externalevent
    ADD CONSTRAINT listings_externalevent_slug_key UNIQUE (slug);


--
-- Name: listings_listing_events listings_listing_events_listing_id_0f94d8c8_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_events
    ADD CONSTRAINT listings_listing_events_listing_id_0f94d8c8_uniq UNIQUE (listing_id, event_id);


--
-- Name: listings_listing_events listings_listing_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_events
    ADD CONSTRAINT listings_listing_events_pkey PRIMARY KEY (id);


--
-- Name: listings_listing_external_events listings_listing_external_events_listing_id_3ed45dca_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_external_events
    ADD CONSTRAINT listings_listing_external_events_listing_id_3ed45dca_uniq UNIQUE (listing_id, externalevent_id);


--
-- Name: listings_listing_external_events listings_listing_external_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_external_events
    ADD CONSTRAINT listings_listing_external_events_pkey PRIMARY KEY (id);


--
-- Name: listings_listing listings_listing_hostname_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing
    ADD CONSTRAINT listings_listing_hostname_key UNIQUE (hostname);


--
-- Name: listings_listing listings_listing_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing
    ADD CONSTRAINT listings_listing_pkey PRIMARY KEY (id);


--
-- Name: mailings_message mailings_message_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_message
    ADD CONSTRAINT mailings_message_pkey PRIMARY KEY (id);


--
-- Name: mailings_personmessage mailings_personmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage
    ADD CONSTRAINT mailings_personmessage_pkey PRIMARY KEY (id);


--
-- Name: mailings_personmessagebody mailings_personmessagebody_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessagebody
    ADD CONSTRAINT mailings_personmessagebody_pkey PRIMARY KEY (id);


--
-- Name: mailings_personmessagesubject mailings_personmessagesubject_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessagesubject
    ADD CONSTRAINT mailings_personmessagesubject_pkey PRIMARY KEY (id);


--
-- Name: mailings_recipientgroup mailings_recipientgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup
    ADD CONSTRAINT mailings_recipientgroup_pkey PRIMARY KEY (id);


--
-- Name: matsucon2018_signupextra matsucon2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra
    ADD CONSTRAINT matsucon2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: matsucon2018_signupextra matsucon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra
    ADD CONSTRAINT matsucon2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: matsucon2018_signupextra_special_diet matsucon2018_signupextra_special_d_signupextra_id_13ad18d6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra_special_diet
    ADD CONSTRAINT matsucon2018_signupextra_special_d_signupextra_id_13ad18d6_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: matsucon2018_signupextra_special_diet matsucon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra_special_diet
    ADD CONSTRAINT matsucon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: membership_membership membership_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membership
    ADD CONSTRAINT membership_membership_pkey PRIMARY KEY (id);


--
-- Name: membership_membershipfeepayment membership_membershipfeepayment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershipfeepayment
    ADD CONSTRAINT membership_membershipfeepayment_pkey PRIMARY KEY (id);


--
-- Name: membership_membershiporganizationmeta membership_membershiporganizationmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershiporganizationmeta
    ADD CONSTRAINT membership_membershiporganizationmeta_pkey PRIMARY KEY (organization_id);


--
-- Name: membership_term membership_term_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_term
    ADD CONSTRAINT membership_term_pkey PRIMARY KEY (id);


--
-- Name: mimicon2016_night mimicon2016_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_night
    ADD CONSTRAINT mimicon2016_night_pkey PRIMARY KEY (id);


--
-- Name: mimicon2016_signupextra_lodging_needs mimicon2016_signupextra_lodging_ne_signupextra_id_537f80b1_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2016_signupextra_lodging_ne_signupextra_id_537f80b1_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: mimicon2016_signupextra_lodging_needs mimicon2016_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2016_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: mimicon2016_signupextra mimicon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra
    ADD CONSTRAINT mimicon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: mimicon2016_signupextra_special_diet mimicon2016_signupextra_special_di_signupextra_id_180e976c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_special_diet
    ADD CONSTRAINT mimicon2016_signupextra_special_di_signupextra_id_180e976c_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: mimicon2016_signupextra_special_diet mimicon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_special_diet
    ADD CONSTRAINT mimicon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: mimicon2016_specialdiet mimicon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_specialdiet
    ADD CONSTRAINT mimicon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: mimicon2018_night mimicon2018_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_night
    ADD CONSTRAINT mimicon2018_night_pkey PRIMARY KEY (id);


--
-- Name: mimicon2018_signupextra_lodging_needs mimicon2018_signupextra_lodging_ne_signupextra_id_46535e02_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2018_signupextra_lodging_ne_signupextra_id_46535e02_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: mimicon2018_signupextra_lodging_needs mimicon2018_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2018_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: mimicon2018_signupextra mimicon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra
    ADD CONSTRAINT mimicon2018_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: mimicon2018_signupextra_special_diet mimicon2018_signupextra_special_di_signupextra_id_7401924a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_special_diet
    ADD CONSTRAINT mimicon2018_signupextra_special_di_signupextra_id_7401924a_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: mimicon2018_signupextra_special_diet mimicon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_special_diet
    ADD CONSTRAINT mimicon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: mimicon2018_specialdiet mimicon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_specialdiet
    ADD CONSTRAINT mimicon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: nexmo_deliverystatusfragment nexmo_deliverystatusfragment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_deliverystatusfragment
    ADD CONSTRAINT nexmo_deliverystatusfragment_pkey PRIMARY KEY (id);


--
-- Name: nexmo_inboundmessage nexmo_inboundmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_inboundmessage
    ADD CONSTRAINT nexmo_inboundmessage_pkey PRIMARY KEY (id);


--
-- Name: nexmo_inboundmessagefragment nexmo_inboundmessagefragment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_inboundmessagefragment
    ADD CONSTRAINT nexmo_inboundmessagefragment_pkey PRIMARY KEY (id);


--
-- Name: nexmo_outboundmessage nexmo_outboundmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_outboundmessage
    ADD CONSTRAINT nexmo_outboundmessage_pkey PRIMARY KEY (id);


--
-- Name: nippori2017_signupextra nippori2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nippori2017_signupextra
    ADD CONSTRAINT nippori2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: nippori2017_signupextra nippori2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nippori2017_signupextra
    ADD CONSTRAINT nippori2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_token_8af090f8_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_token_8af090f8_uniq UNIQUE (token);


--
-- Name: oauth2_provider_application oauth2_provider_application_client_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_client_id_key UNIQUE (client_id);


--
-- Name: oauth2_provider_application oauth2_provider_application_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_grant oauth2_provider_grant_code_49ab4ddf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_code_49ab4ddf_uniq UNIQUE (code);


--
-- Name: oauth2_provider_grant oauth2_provider_grant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_access_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_access_token_id_key UNIQUE (access_token_id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_pkey PRIMARY KEY (id);


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_token_d090daa4_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_token_d090daa4_uniq UNIQUE (token);


--
-- Name: payments_payment payments_payment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_pkey PRIMARY KEY (id);


--
-- Name: payments_paymentseventmeta payments_paymentseventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_paymentseventmeta
    ADD CONSTRAINT payments_paymentseventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: popcult2017_signupextra popcult2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra
    ADD CONSTRAINT popcult2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: popcult2017_signupextra popcult2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra
    ADD CONSTRAINT popcult2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: popcult2017_signupextra_special_diet popcult2017_signupextra_special_di_signupextra_id_cc3e0895_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra_special_diet
    ADD CONSTRAINT popcult2017_signupextra_special_di_signupextra_id_cc3e0895_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: popcult2017_signupextra_special_diet popcult2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra_special_diet
    ADD CONSTRAINT popcult2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: popcultday2018_signupextra popcultday2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra
    ADD CONSTRAINT popcultday2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: popcultday2018_signupextra popcultday2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra
    ADD CONSTRAINT popcultday2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: popcultday2018_signupextra_special_diet popcultday2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra_special_diet
    ADD CONSTRAINT popcultday2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: popcultday2018_signupextra_special_diet popcultday2018_signupextra_special_signupextra_id_f1f50c89_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra_special_diet
    ADD CONSTRAINT popcultday2018_signupextra_special_signupextra_id_f1f50c89_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: programme_alternativeprogrammeform programme_alternativeprogrammeform_event_id_640ef52c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_alternativeprogrammeform
    ADD CONSTRAINT programme_alternativeprogrammeform_event_id_640ef52c_uniq UNIQUE (event_id, slug);


--
-- Name: programme_alternativeprogrammeform programme_alternativeprogrammeform_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_alternativeprogrammeform
    ADD CONSTRAINT programme_alternativeprogrammeform_pkey PRIMARY KEY (id);


--
-- Name: programme_category programme_category_event_id_f6f90e42_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_category
    ADD CONSTRAINT programme_category_event_id_f6f90e42_uniq UNIQUE (event_id, slug);


--
-- Name: programme_category programme_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_category
    ADD CONSTRAINT programme_category_pkey PRIMARY KEY (id);


--
-- Name: programme_freeformorganizer programme_freeformorganizer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_freeformorganizer
    ADD CONSTRAINT programme_freeformorganizer_pkey PRIMARY KEY (id);


--
-- Name: programme_invitation programme_invitation_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invitation_code_key UNIQUE (code);


--
-- Name: programme_invitation programme_invitation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invitation_pkey PRIMARY KEY (id);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots programme_programme_hitpoint2017_pre_programme_id_c85075b9_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_hitpoint2017_preferred_time_slots
    ADD CONSTRAINT programme_programme_hitpoint2017_pre_programme_id_c85075b9_uniq UNIQUE (programme_id, timeslot_id);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots programme_programme_hitpoint2017_preferred_time_slots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_hitpoint2017_preferred_time_slots
    ADD CONSTRAINT programme_programme_hitpoint2017_preferred_time_slots_pkey PRIMARY KEY (id);


--
-- Name: programme_programme programme_programme_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme
    ADD CONSTRAINT programme_programme_pkey PRIMARY KEY (id);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots programme_programme_ropecon2018_pref_programme_id_bb2edc4f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_ropecon2018_preferred_time_slots
    ADD CONSTRAINT programme_programme_ropecon2018_pref_programme_id_bb2edc4f_uniq UNIQUE (programme_id, timeslot_id);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots programme_programme_ropecon2018_preferred_time_slots_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_ropecon2018_preferred_time_slots
    ADD CONSTRAINT programme_programme_ropecon2018_preferred_time_slots_pkey PRIMARY KEY (id);


--
-- Name: programme_programme_tags programme_programme_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_tags
    ADD CONSTRAINT programme_programme_tags_pkey PRIMARY KEY (id);


--
-- Name: programme_programme_tags programme_programme_tags_programme_id_630727ea_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_tags
    ADD CONSTRAINT programme_programme_tags_programme_id_630727ea_uniq UNIQUE (programme_id, tag_id);


--
-- Name: programme_programmeeventmeta programme_programmeeventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmeeventmeta
    ADD CONSTRAINT programme_programmeeventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: programme_programmefeedback programme_programmefeedback_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmefeedback
    ADD CONSTRAINT programme_programmefeedback_pkey PRIMARY KEY (id);


--
-- Name: programme_programmerole programme_programmerole_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole
    ADD CONSTRAINT programme_programmerole_pkey PRIMARY KEY (id);


--
-- Name: programme_role programme_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_role
    ADD CONSTRAINT programme_role_pkey PRIMARY KEY (id);


--
-- Name: programme_room programme_room_event_id_86fc4ec4_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_room
    ADD CONSTRAINT programme_room_event_id_86fc4ec4_uniq UNIQUE (event_id, slug);


--
-- Name: programme_room programme_room_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_room
    ADD CONSTRAINT programme_room_pkey PRIMARY KEY (id);


--
-- Name: programme_specialstarttime programme_specialstarttime_event_id_d7d243fb_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_specialstarttime
    ADD CONSTRAINT programme_specialstarttime_event_id_d7d243fb_uniq UNIQUE (event_id, start_time);


--
-- Name: programme_specialstarttime programme_specialstarttime_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_specialstarttime
    ADD CONSTRAINT programme_specialstarttime_pkey PRIMARY KEY (id);


--
-- Name: programme_tag programme_tag_event_id_a5205bf2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_tag
    ADD CONSTRAINT programme_tag_event_id_a5205bf2_uniq UNIQUE (event_id, slug);


--
-- Name: programme_tag programme_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_tag
    ADD CONSTRAINT programme_tag_pkey PRIMARY KEY (id);


--
-- Name: programme_timeblock programme_timeblock_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_timeblock
    ADD CONSTRAINT programme_timeblock_pkey PRIMARY KEY (id);


--
-- Name: programme_view programme_view_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_view
    ADD CONSTRAINT programme_view_pkey PRIMARY KEY (id);


--
-- Name: programme_viewroom programme_viewroom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_viewroom
    ADD CONSTRAINT programme_viewroom_pkey PRIMARY KEY (id);


--
-- Name: ropecon2018_signupextra ropecon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra
    ADD CONSTRAINT ropecon2018_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: ropecon2018_signupextra_special_diet ropecon2018_signupextra_special_di_signupextra_id_a21472b3_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra_special_diet
    ADD CONSTRAINT ropecon2018_signupextra_special_di_signupextra_id_a21472b3_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: ropecon2018_signupextra_special_diet ropecon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra_special_diet
    ADD CONSTRAINT ropecon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: ropecon2018_specialdiet ropecon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_specialdiet
    ADD CONSTRAINT ropecon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: ropecon2018_timeslot ropecon2018_timeslot_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_timeslot
    ADD CONSTRAINT ropecon2018_timeslot_pkey PRIMARY KEY (id);


--
-- Name: shippocon2016_signupextra shippocon2016_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra
    ADD CONSTRAINT shippocon2016_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: shippocon2016_signupextra shippocon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra
    ADD CONSTRAINT shippocon2016_signupextra_pkey PRIMARY KEY (id);


--
-- Name: shippocon2016_signupextra_special_diet shippocon2016_signupextra_special__signupextra_id_94a0b17c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra_special_diet
    ADD CONSTRAINT shippocon2016_signupextra_special__signupextra_id_94a0b17c_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: shippocon2016_signupextra_special_diet shippocon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra_special_diet
    ADD CONSTRAINT shippocon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: shippocon2016_specialdiet shippocon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_specialdiet
    ADD CONSTRAINT shippocon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: sms_hotword sms_hotword_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_hotword
    ADD CONSTRAINT sms_hotword_pkey PRIMARY KEY (id);


--
-- Name: sms_nominee_category sms_nominee_category_nominee_id_6331eadd_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee_category
    ADD CONSTRAINT sms_nominee_category_nominee_id_6331eadd_uniq UNIQUE (nominee_id, votecategory_id);


--
-- Name: sms_nominee_category sms_nominee_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee_category
    ADD CONSTRAINT sms_nominee_category_pkey PRIMARY KEY (id);


--
-- Name: sms_nominee sms_nominee_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee
    ADD CONSTRAINT sms_nominee_pkey PRIMARY KEY (id);


--
-- Name: sms_smseventmeta sms_smseventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smseventmeta
    ADD CONSTRAINT sms_smseventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: sms_smsmessagein sms_smsmessagein_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessagein
    ADD CONSTRAINT sms_smsmessagein_pkey PRIMARY KEY (id);


--
-- Name: sms_smsmessageout sms_smsmessageout_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessageout
    ADD CONSTRAINT sms_smsmessageout_pkey PRIMARY KEY (id);


--
-- Name: sms_vote sms_vote_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_vote
    ADD CONSTRAINT sms_vote_pkey PRIMARY KEY (id);


--
-- Name: sms_votecategory sms_votecategory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_votecategory
    ADD CONSTRAINT sms_votecategory_pkey PRIMARY KEY (id);


--
-- Name: surveys_eventsurvey surveys_eventsurvey_event_id_c0f2019c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurvey
    ADD CONSTRAINT surveys_eventsurvey_event_id_c0f2019c_uniq UNIQUE (event_id, slug);


--
-- Name: surveys_eventsurvey surveys_eventsurvey_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurvey
    ADD CONSTRAINT surveys_eventsurvey_pkey PRIMARY KEY (id);


--
-- Name: surveys_eventsurveyresult surveys_eventsurveyresult_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurveyresult
    ADD CONSTRAINT surveys_eventsurveyresult_pkey PRIMARY KEY (id);


--
-- Name: surveys_globalsurvey surveys_globalsurvey_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurvey
    ADD CONSTRAINT surveys_globalsurvey_pkey PRIMARY KEY (id);


--
-- Name: surveys_globalsurvey surveys_globalsurvey_slug_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurvey
    ADD CONSTRAINT surveys_globalsurvey_slug_key UNIQUE (slug);


--
-- Name: surveys_globalsurveyresult surveys_globalsurveyresult_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurveyresult
    ADD CONSTRAINT surveys_globalsurveyresult_pkey PRIMARY KEY (id);


--
-- Name: tickets_accommodationinformation_limit_groups tickets_accommodation_accommodationinformation_id_f437e8e6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation_limit_groups
    ADD CONSTRAINT tickets_accommodation_accommodationinformation_id_f437e8e6_uniq UNIQUE (accommodationinformation_id, limitgroup_id);


--
-- Name: tickets_accommodationinformation_limit_groups tickets_accommodationinformation_limit_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation_limit_groups
    ADD CONSTRAINT tickets_accommodationinformation_limit_groups_pkey PRIMARY KEY (id);


--
-- Name: tickets_accommodationinformation tickets_accommodationinformation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation
    ADD CONSTRAINT tickets_accommodationinformation_pkey PRIMARY KEY (id);


--
-- Name: tickets_batch tickets_batch_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_batch
    ADD CONSTRAINT tickets_batch_pkey PRIMARY KEY (id);


--
-- Name: tickets_customer tickets_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_customer
    ADD CONSTRAINT tickets_customer_pkey PRIMARY KEY (id);


--
-- Name: tickets_limitgroup tickets_limitgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_limitgroup
    ADD CONSTRAINT tickets_limitgroup_pkey PRIMARY KEY (id);


--
-- Name: tickets_order tickets_order_customer_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order
    ADD CONSTRAINT tickets_order_customer_id_key UNIQUE (customer_id);


--
-- Name: tickets_order tickets_order_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order
    ADD CONSTRAINT tickets_order_pkey PRIMARY KEY (id);


--
-- Name: tickets_orderproduct tickets_orderproduct_order_id_dfb99eee_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_orderproduct
    ADD CONSTRAINT tickets_orderproduct_order_id_dfb99eee_uniq UNIQUE (order_id, product_id);


--
-- Name: tickets_orderproduct tickets_orderproduct_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_orderproduct
    ADD CONSTRAINT tickets_orderproduct_pkey PRIMARY KEY (id);


--
-- Name: tickets_product_limit_groups tickets_product_limit_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product_limit_groups
    ADD CONSTRAINT tickets_product_limit_groups_pkey PRIMARY KEY (id);


--
-- Name: tickets_product_limit_groups tickets_product_limit_groups_product_id_87f1916e_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product_limit_groups
    ADD CONSTRAINT tickets_product_limit_groups_product_id_87f1916e_uniq UNIQUE (product_id, limitgroup_id);


--
-- Name: tickets_product tickets_product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product
    ADD CONSTRAINT tickets_product_pkey PRIMARY KEY (id);


--
-- Name: tickets_shirtorder tickets_shirtorder_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtorder
    ADD CONSTRAINT tickets_shirtorder_pkey PRIMARY KEY (id);


--
-- Name: tickets_shirtsize tickets_shirtsize_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtsize
    ADD CONSTRAINT tickets_shirtsize_pkey PRIMARY KEY (id);


--
-- Name: tickets_shirtsize tickets_shirtsize_type_id_81460153_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtsize
    ADD CONSTRAINT tickets_shirtsize_type_id_81460153_uniq UNIQUE (type_id, slug);


--
-- Name: tickets_shirttype tickets_shirttype_event_id_c5c43e83_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirttype
    ADD CONSTRAINT tickets_shirttype_event_id_c5c43e83_uniq UNIQUE (event_id, slug);


--
-- Name: tickets_shirttype tickets_shirttype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirttype
    ADD CONSTRAINT tickets_shirttype_pkey PRIMARY KEY (id);


--
-- Name: tickets_ticketseventmeta tickets_ticketseventmeta_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_ticketseventmeta
    ADD CONSTRAINT tickets_ticketseventmeta_pkey PRIMARY KEY (event_id);


--
-- Name: tracon11_night tracon11_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_night
    ADD CONSTRAINT tracon11_night_pkey PRIMARY KEY (id);


--
-- Name: tracon11_signupextra_lodging_needs tracon11_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_lodging_needs
    ADD CONSTRAINT tracon11_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: tracon11_signupextra_lodging_needs tracon11_signupextra_lodging_needs_signupextra_id_dde5e188_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_lodging_needs
    ADD CONSTRAINT tracon11_signupextra_lodging_needs_signupextra_id_dde5e188_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: tracon11_signupextra tracon11_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra
    ADD CONSTRAINT tracon11_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: tracon11_signupextra_special_diet tracon11_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_special_diet
    ADD CONSTRAINT tracon11_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tracon11_signupextra_special_diet tracon11_signupextra_special_diet_signupextra_id_1daeccd2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_special_diet
    ADD CONSTRAINT tracon11_signupextra_special_diet_signupextra_id_1daeccd2_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: tracon11_signupextrav2_lodging_needs tracon11_signupextrav2_lodging_n_signupextrav2_id_39b82895_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_lodging_needs
    ADD CONSTRAINT tracon11_signupextrav2_lodging_n_signupextrav2_id_39b82895_uniq UNIQUE (signupextrav2_id, night_id);


--
-- Name: tracon11_signupextrav2_lodging_needs tracon11_signupextrav2_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_lodging_needs
    ADD CONSTRAINT tracon11_signupextrav2_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: tracon11_signupextrav2 tracon11_signupextrav2_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2
    ADD CONSTRAINT tracon11_signupextrav2_person_id_key UNIQUE (person_id);


--
-- Name: tracon11_signupextrav2 tracon11_signupextrav2_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2
    ADD CONSTRAINT tracon11_signupextrav2_pkey PRIMARY KEY (id);


--
-- Name: tracon11_signupextrav2_special_diet tracon11_signupextrav2_special_d_signupextrav2_id_9fc0c502_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_special_diet
    ADD CONSTRAINT tracon11_signupextrav2_special_d_signupextrav2_id_9fc0c502_uniq UNIQUE (signupextrav2_id, specialdiet_id);


--
-- Name: tracon11_signupextrav2_special_diet tracon11_signupextrav2_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_special_diet
    ADD CONSTRAINT tracon11_signupextrav2_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tracon11_specialdiet tracon11_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_specialdiet
    ADD CONSTRAINT tracon11_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_night tracon2017_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_night
    ADD CONSTRAINT tracon2017_night_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_poison tracon2017_poison_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_poison
    ADD CONSTRAINT tracon2017_poison_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_signupextra_lodging_needs tracon2017_signupextra_lodging_nee_signupextra_id_7d8be596_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_lodging_needs
    ADD CONSTRAINT tracon2017_signupextra_lodging_nee_signupextra_id_7d8be596_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: tracon2017_signupextra_lodging_needs tracon2017_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_lodging_needs
    ADD CONSTRAINT tracon2017_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_signupextra tracon2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra
    ADD CONSTRAINT tracon2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: tracon2017_signupextra_pick_your_poison tracon2017_signupextra_pick_your_p_signupextra_id_35724908_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2017_signupextra_pick_your_p_signupextra_id_35724908_uniq UNIQUE (signupextra_id, poison_id);


--
-- Name: tracon2017_signupextra_pick_your_poison tracon2017_signupextra_pick_your_poison_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2017_signupextra_pick_your_poison_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_signupextra tracon2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra
    ADD CONSTRAINT tracon2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: tracon2017_signupextra_special_diet tracon2017_signupextra_special_die_signupextra_id_22b38fe5_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_special_diet
    ADD CONSTRAINT tracon2017_signupextra_special_die_signupextra_id_22b38fe5_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: tracon2017_signupextra_special_diet tracon2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_special_diet
    ADD CONSTRAINT tracon2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_night tracon2018_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_night
    ADD CONSTRAINT tracon2018_night_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_poison tracon2018_poison_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_poison
    ADD CONSTRAINT tracon2018_poison_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_signupextra_lodging_needs tracon2018_signupextra_lodging_nee_signupextra_id_bfd2ced2_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_lodging_needs
    ADD CONSTRAINT tracon2018_signupextra_lodging_nee_signupextra_id_bfd2ced2_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: tracon2018_signupextra_lodging_needs tracon2018_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_lodging_needs
    ADD CONSTRAINT tracon2018_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_signupextra tracon2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra
    ADD CONSTRAINT tracon2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: tracon2018_signupextra_pick_your_poison tracon2018_signupextra_pick_your_p_signupextra_id_e4d5bef6_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2018_signupextra_pick_your_p_signupextra_id_e4d5bef6_uniq UNIQUE (signupextra_id, poison_id);


--
-- Name: tracon2018_signupextra_pick_your_poison tracon2018_signupextra_pick_your_poison_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2018_signupextra_pick_your_poison_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_signupextra tracon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra
    ADD CONSTRAINT tracon2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: tracon2018_signupextra_special_diet tracon2018_signupextra_special_die_signupextra_id_a33bb21e_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_special_diet
    ADD CONSTRAINT tracon2018_signupextra_special_die_signupextra_id_a33bb21e_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: tracon2018_signupextra_special_diet tracon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_special_diet
    ADD CONSTRAINT tracon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tracon9_night tracon9_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_night
    ADD CONSTRAINT tracon9_night_pkey PRIMARY KEY (id);


--
-- Name: tracon9_signupextra_lodging_needs tracon9_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_lodging_needs
    ADD CONSTRAINT tracon9_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: tracon9_signupextra_lodging_needs tracon9_signupextra_lodging_needs_signupextra_id_87eac79b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_lodging_needs
    ADD CONSTRAINT tracon9_signupextra_lodging_needs_signupextra_id_87eac79b_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: tracon9_signupextra tracon9_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra
    ADD CONSTRAINT tracon9_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: tracon9_signupextra_special_diet tracon9_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_special_diet
    ADD CONSTRAINT tracon9_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tracon9_signupextra_special_diet tracon9_signupextra_special_diet_signupextra_id_29f2ed0d_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_special_diet
    ADD CONSTRAINT tracon9_signupextra_special_diet_signupextra_id_29f2ed0d_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: tracon9_specialdiet tracon9_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_specialdiet
    ADD CONSTRAINT tracon9_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: traconx_night traconx_night_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_night
    ADD CONSTRAINT traconx_night_pkey PRIMARY KEY (id);


--
-- Name: traconx_signupextra_lodging_needs traconx_signupextra_lodging_needs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_lodging_needs
    ADD CONSTRAINT traconx_signupextra_lodging_needs_pkey PRIMARY KEY (id);


--
-- Name: traconx_signupextra_lodging_needs traconx_signupextra_lodging_needs_signupextra_id_f931d91c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_lodging_needs
    ADD CONSTRAINT traconx_signupextra_lodging_needs_signupextra_id_f931d91c_uniq UNIQUE (signupextra_id, night_id);


--
-- Name: traconx_signupextra traconx_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra
    ADD CONSTRAINT traconx_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: traconx_signupextra_special_diet traconx_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_special_diet
    ADD CONSTRAINT traconx_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: traconx_signupextra_special_diet traconx_signupextra_special_diet_signupextra_id_5c95bedf_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_special_diet
    ADD CONSTRAINT traconx_signupextra_special_diet_signupextra_id_5c95bedf_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: traconx_specialdiet traconx_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_specialdiet
    ADD CONSTRAINT traconx_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: tylycon2017_signupextra tylycon2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra
    ADD CONSTRAINT tylycon2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: tylycon2017_signupextra tylycon2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra
    ADD CONSTRAINT tylycon2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: tylycon2017_signupextra_special_diet tylycon2017_signupextra_special_di_signupextra_id_c290076e_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra_special_diet
    ADD CONSTRAINT tylycon2017_signupextra_special_di_signupextra_id_c290076e_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: tylycon2017_signupextra_special_diet tylycon2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra_special_diet
    ADD CONSTRAINT tylycon2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: tylycon2017_specialdiet tylycon2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_specialdiet
    ADD CONSTRAINT tylycon2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: worldcon75_signupextra worldcon75_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra
    ADD CONSTRAINT worldcon75_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: worldcon75_signupextra worldcon75_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra
    ADD CONSTRAINT worldcon75_signupextra_pkey PRIMARY KEY (id);


--
-- Name: worldcon75_signupextra_special_diet worldcon75_signupextra_special_die_signupextra_id_e3e330dc_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra_special_diet
    ADD CONSTRAINT worldcon75_signupextra_special_die_signupextra_id_e3e330dc_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: worldcon75_signupextra_special_diet worldcon75_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra_special_diet
    ADD CONSTRAINT worldcon75_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2016_signupextra yukicon2016_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra
    ADD CONSTRAINT yukicon2016_signupextra_pkey PRIMARY KEY (signup_id);


--
-- Name: yukicon2016_signupextra_special_diet yukicon2016_signupextra_special_di_signupextra_id_69eb483f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra_special_diet
    ADD CONSTRAINT yukicon2016_signupextra_special_di_signupextra_id_69eb483f_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: yukicon2016_signupextra_special_diet yukicon2016_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra_special_diet
    ADD CONSTRAINT yukicon2016_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2016_specialdiet yukicon2016_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_specialdiet
    ADD CONSTRAINT yukicon2016_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2017_eventday yukicon2017_eventday_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_eventday
    ADD CONSTRAINT yukicon2017_eventday_pkey PRIMARY KEY (id);


--
-- Name: yukicon2017_signupextra yukicon2017_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra
    ADD CONSTRAINT yukicon2017_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: yukicon2017_signupextra yukicon2017_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra
    ADD CONSTRAINT yukicon2017_signupextra_pkey PRIMARY KEY (id);


--
-- Name: yukicon2017_signupextra_special_diet yukicon2017_signupextra_special_di_signupextra_id_8c2f3d9c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_special_diet
    ADD CONSTRAINT yukicon2017_signupextra_special_di_signupextra_id_8c2f3d9c_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: yukicon2017_signupextra_special_diet yukicon2017_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_special_diet
    ADD CONSTRAINT yukicon2017_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2017_signupextra_work_days yukicon2017_signupextra_work_days_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_work_days
    ADD CONSTRAINT yukicon2017_signupextra_work_days_pkey PRIMARY KEY (id);


--
-- Name: yukicon2017_signupextra_work_days yukicon2017_signupextra_work_days_signupextra_id_c8fc0743_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_work_days
    ADD CONSTRAINT yukicon2017_signupextra_work_days_signupextra_id_c8fc0743_uniq UNIQUE (signupextra_id, eventday_id);


--
-- Name: yukicon2017_specialdiet yukicon2017_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_specialdiet
    ADD CONSTRAINT yukicon2017_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2018_eventday yukicon2018_eventday_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_eventday
    ADD CONSTRAINT yukicon2018_eventday_pkey PRIMARY KEY (id);


--
-- Name: yukicon2018_signupextra yukicon2018_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra
    ADD CONSTRAINT yukicon2018_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: yukicon2018_signupextra yukicon2018_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra
    ADD CONSTRAINT yukicon2018_signupextra_pkey PRIMARY KEY (id);


--
-- Name: yukicon2018_signupextra_special_diet yukicon2018_signupextra_special_di_signupextra_id_3ce8eca9_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_special_diet
    ADD CONSTRAINT yukicon2018_signupextra_special_di_signupextra_id_3ce8eca9_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: yukicon2018_signupextra_special_diet yukicon2018_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_special_diet
    ADD CONSTRAINT yukicon2018_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2018_signupextra_work_days yukicon2018_signupextra_work_days_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_work_days
    ADD CONSTRAINT yukicon2018_signupextra_work_days_pkey PRIMARY KEY (id);


--
-- Name: yukicon2018_signupextra_work_days yukicon2018_signupextra_work_days_signupextra_id_2e6db54f_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_work_days
    ADD CONSTRAINT yukicon2018_signupextra_work_days_signupextra_id_2e6db54f_uniq UNIQUE (signupextra_id, eventday_id);


--
-- Name: yukicon2018_specialdiet yukicon2018_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_specialdiet
    ADD CONSTRAINT yukicon2018_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2019_eventday yukicon2019_eventday_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_eventday
    ADD CONSTRAINT yukicon2019_eventday_pkey PRIMARY KEY (id);


--
-- Name: yukicon2019_signupextra yukicon2019_signupextra_person_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra
    ADD CONSTRAINT yukicon2019_signupextra_person_id_key UNIQUE (person_id);


--
-- Name: yukicon2019_signupextra yukicon2019_signupextra_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra
    ADD CONSTRAINT yukicon2019_signupextra_pkey PRIMARY KEY (id);


--
-- Name: yukicon2019_signupextra_special_diet yukicon2019_signupextra_special_di_signupextra_id_4997b8e9_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_special_diet
    ADD CONSTRAINT yukicon2019_signupextra_special_di_signupextra_id_4997b8e9_uniq UNIQUE (signupextra_id, specialdiet_id);


--
-- Name: yukicon2019_signupextra_special_diet yukicon2019_signupextra_special_diet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_special_diet
    ADD CONSTRAINT yukicon2019_signupextra_special_diet_pkey PRIMARY KEY (id);


--
-- Name: yukicon2019_signupextra_work_days yukicon2019_signupextra_work_days_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_work_days
    ADD CONSTRAINT yukicon2019_signupextra_work_days_pkey PRIMARY KEY (id);


--
-- Name: yukicon2019_signupextra_work_days yukicon2019_signupextra_work_days_signupextra_id_6440c598_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_work_days
    ADD CONSTRAINT yukicon2019_signupextra_work_days_signupextra_id_6440c598_uniq UNIQUE (signupextra_id, eventday_id);


--
-- Name: yukicon2019_specialdiet yukicon2019_specialdiet_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_specialdiet
    ADD CONSTRAINT yukicon2019_specialdiet_pkey PRIMARY KEY (id);


--
-- Name: access_accessorganizationmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_accessorganizationmeta_0a405bd6 ON public.access_accessorganizationmeta USING btree (admin_group_id);


--
-- Name: access_emailalias_662cbf12; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailalias_662cbf12 ON public.access_emailalias USING btree (domain_id);


--
-- Name: access_emailalias_94757cae; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailalias_94757cae ON public.access_emailalias USING btree (type_id);


--
-- Name: access_emailalias_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailalias_a8452ca7 ON public.access_emailalias USING btree (person_id);


--
-- Name: access_emailalias_e4795667; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailalias_e4795667 ON public.access_emailalias USING btree (group_grant_id);


--
-- Name: access_emailaliasdomain_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailaliasdomain_26b2345e ON public.access_emailaliasdomain USING btree (organization_id);


--
-- Name: access_emailaliasdomain_domain_name_a0a33fc7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailaliasdomain_domain_name_a0a33fc7_like ON public.access_emailaliasdomain USING btree (domain_name varchar_pattern_ops);


--
-- Name: access_emailaliastype_662cbf12; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_emailaliastype_662cbf12 ON public.access_emailaliastype USING btree (domain_id);


--
-- Name: access_grantedprivilege_a3783896; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_grantedprivilege_a3783896 ON public.access_grantedprivilege USING btree (privilege_id);


--
-- Name: access_grantedprivilege_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_grantedprivilege_a8452ca7 ON public.access_grantedprivilege USING btree (person_id);


--
-- Name: access_groupemailaliasgrant_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_groupemailaliasgrant_0e939a4f ON public.access_groupemailaliasgrant USING btree (group_id);


--
-- Name: access_groupemailaliasgrant_94757cae; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_groupemailaliasgrant_94757cae ON public.access_groupemailaliasgrant USING btree (type_id);


--
-- Name: access_groupprivilege_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_groupprivilege_0e939a4f ON public.access_groupprivilege USING btree (group_id);


--
-- Name: access_groupprivilege_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_groupprivilege_4437cfac ON public.access_groupprivilege USING btree (event_id);


--
-- Name: access_groupprivilege_a3783896; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_groupprivilege_a3783896 ON public.access_groupprivilege USING btree (privilege_id);


--
-- Name: access_internalemailalias_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_internalemailalias_4437cfac ON public.access_internalemailalias USING btree (event_id);


--
-- Name: access_internalemailalias_662cbf12; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_internalemailalias_662cbf12 ON public.access_internalemailalias USING btree (domain_id);


--
-- Name: access_privilege_slug_4cf01a26_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_privilege_slug_4cf01a26_like ON public.access_privilege USING btree (slug varchar_pattern_ops);


--
-- Name: access_smtppassword_9548f59c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_smtppassword_9548f59c ON public.access_smtppassword USING btree (smtp_server_id);


--
-- Name: access_smtppassword_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_smtppassword_a8452ca7 ON public.access_smtppassword USING btree (person_id);


--
-- Name: access_smtpserver_domains_1993bf2a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_smtpserver_domains_1993bf2a ON public.access_smtpserver_domains USING btree (smtpserver_id);


--
-- Name: access_smtpserver_domains_5defd3e8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX access_smtpserver_domains_5defd3e8 ON public.access_smtpserver_domains USING btree (emailaliasdomain_id);


--
-- Name: aicon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX aicon2016_signupextra_special_diet_42414328 ON public.aicon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: aicon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX aicon2016_signupextra_special_diet_d37df680 ON public.aicon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: aicon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX aicon2018_signupextra_special_diet_42414328 ON public.aicon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: aicon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX aicon2018_signupextra_special_diet_d37df680 ON public.aicon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: animecon2015_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2015_signupextra_lodging_needs_42414328 ON public.animecon2015_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: animecon2015_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2015_signupextra_lodging_needs_a9142bf0 ON public.animecon2015_signupextra_lodging_needs USING btree (night_id);


--
-- Name: animecon2015_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2015_signupextra_special_diet_42414328 ON public.animecon2015_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: animecon2015_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2015_signupextra_special_diet_d37df680 ON public.animecon2015_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: animecon2016_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2016_signupextra_lodging_needs_42414328 ON public.animecon2016_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: animecon2016_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2016_signupextra_lodging_needs_a9142bf0 ON public.animecon2016_signupextra_lodging_needs USING btree (night_id);


--
-- Name: animecon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2016_signupextra_special_diet_42414328 ON public.animecon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: animecon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX animecon2016_signupextra_special_diet_d37df680 ON public.animecon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_0e939a4f ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_8373b171 ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_417f1b1c ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_0e939a4f ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_e8701ad4 ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_8373b171 ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: badges_badge_87104232; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badge_87104232 ON public.badges_badge USING btree (revoked_by_id);


--
-- Name: badges_badge_a074c466; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badge_a074c466 ON public.badges_badge USING btree (personnel_class_id);


--
-- Name: badges_badge_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badge_a8452ca7 ON public.badges_badge USING btree (person_id);


--
-- Name: badges_badge_d4e60137; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badge_d4e60137 ON public.badges_badge USING btree (batch_id);


--
-- Name: badges_badge_e93cb7eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badge_e93cb7eb ON public.badges_badge USING btree (created_by_id);


--
-- Name: badges_badgeseventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_badgeseventmeta_0a405bd6 ON public.badges_badgeseventmeta USING btree (admin_group_id);


--
-- Name: badges_batch_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_batch_4437cfac ON public.badges_batch USING btree (event_id);


--
-- Name: badges_batch_a074c466; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX badges_batch_a074c466 ON public.badges_batch USING btree (personnel_class_id);


--
-- Name: core_emailverificationtoken_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_emailverificationtoken_a8452ca7 ON public.core_emailverificationtoken USING btree (person_id);


--
-- Name: core_emailverificationtoken_code_058f42bf_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_emailverificationtoken_code_058f42bf_like ON public.core_emailverificationtoken USING btree (code varchar_pattern_ops);


--
-- Name: core_emailverificationtoken_person_id_504d87f6_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_emailverificationtoken_person_id_504d87f6_idx ON public.core_emailverificationtoken USING btree (person_id, state);


--
-- Name: core_event_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_event_26b2345e ON public.core_event USING btree (organization_id);


--
-- Name: core_event_f3a4803c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_event_f3a4803c ON public.core_event USING btree (venue_id);


--
-- Name: core_event_slug_cb4996eb_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_event_slug_cb4996eb_like ON public.core_event USING btree (slug varchar_pattern_ops);


--
-- Name: core_organization_slug_d23b3126_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_organization_slug_d23b3126_like ON public.core_organization USING btree (slug varchar_pattern_ops);


--
-- Name: core_passwordresettoken_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_passwordresettoken_a8452ca7 ON public.core_passwordresettoken USING btree (person_id);


--
-- Name: core_passwordresettoken_code_5d6e960c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_passwordresettoken_code_5d6e960c_like ON public.core_passwordresettoken USING btree (code varchar_pattern_ops);


--
-- Name: core_passwordresettoken_person_id_b727e8c1_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX core_passwordresettoken_person_id_b727e8c1_idx ON public.core_passwordresettoken USING btree (person_id, state);


--
-- Name: desucon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2016_signupextra_special_diet_42414328 ON public.desucon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: desucon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2016_signupextra_special_diet_d37df680 ON public.desucon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: desucon2016_signupextrav2_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2016_signupextrav2_4437cfac ON public.desucon2016_signupextrav2 USING btree (event_id);


--
-- Name: desucon2016_signupextrav2_special_diet_328bf3a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2016_signupextrav2_special_diet_328bf3a7 ON public.desucon2016_signupextrav2_special_diet USING btree (signupextrav2_id);


--
-- Name: desucon2016_signupextrav2_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2016_signupextrav2_special_diet_d37df680 ON public.desucon2016_signupextrav2_special_diet USING btree (specialdiet_id);


--
-- Name: desucon2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2017_signupextra_4437cfac ON public.desucon2017_signupextra USING btree (event_id);


--
-- Name: desucon2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2017_signupextra_special_diet_42414328 ON public.desucon2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: desucon2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2017_signupextra_special_diet_d37df680 ON public.desucon2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: desucon2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2018_signupextra_4437cfac ON public.desucon2018_signupextra USING btree (event_id);


--
-- Name: desucon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2018_signupextra_special_diet_42414328 ON public.desucon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: desucon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2018_signupextra_special_diet_d37df680 ON public.desucon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: desucon2019_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2019_signupextra_4437cfac ON public.desucon2019_signupextra USING btree (event_id);


--
-- Name: desucon2019_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2019_signupextra_special_diet_42414328 ON public.desucon2019_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: desucon2019_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desucon2019_signupextra_special_diet_d37df680 ON public.desucon2019_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: desuprofile_integration_confirmationcode_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desuprofile_integration_confirmationcode_a8452ca7 ON public.desuprofile_integration_confirmationcode USING btree (person_id);


--
-- Name: desuprofile_integration_confirmationcode_code_b91a1441_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desuprofile_integration_confirmationcode_code_b91a1441_like ON public.desuprofile_integration_confirmationcode USING btree (code varchar_pattern_ops);


--
-- Name: desuprofile_integration_confirmationcode_person_id_756dd8a0_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX desuprofile_integration_confirmationcode_person_id_756dd8a0_idx ON public.desuprofile_integration_confirmationcode USING btree (person_id, state);


--
-- Name: directory_directoryaccessgroup_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX directory_directoryaccessgroup_0e939a4f ON public.directory_directoryaccessgroup USING btree (group_id);


--
-- Name: directory_directoryaccessgroup_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX directory_directoryaccessgroup_26b2345e ON public.directory_directoryaccessgroup USING btree (organization_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_417f1b1c ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_e8701ad4 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_de54fa62 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: django_site_domain_a2e37b91_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);


--
-- Name: enrollment_enrollment_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_4437cfac ON public.enrollment_enrollment USING btree (event_id);


--
-- Name: enrollment_enrollment_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_a8452ca7 ON public.enrollment_enrollment USING btree (person_id);


--
-- Name: enrollment_enrollment_concon_parts_537d5933; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_concon_parts_537d5933 ON public.enrollment_enrollment_concon_parts USING btree (enrollment_id);


--
-- Name: enrollment_enrollment_concon_parts_acd061c6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_concon_parts_acd061c6 ON public.enrollment_enrollment_concon_parts USING btree (conconpart_id);


--
-- Name: enrollment_enrollment_special_diet_537d5933; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_special_diet_537d5933 ON public.enrollment_enrollment_special_diet USING btree (enrollment_id);


--
-- Name: enrollment_enrollment_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollment_special_diet_d37df680 ON public.enrollment_enrollment_special_diet USING btree (specialdiet_id);


--
-- Name: enrollment_enrollmenteventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX enrollment_enrollmenteventmeta_0a405bd6 ON public.enrollment_enrollmenteventmeta USING btree (admin_group_id);


--
-- Name: event_log_entry_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_26b2345e ON public.event_log_entry USING btree (organization_id);


--
-- Name: event_log_entry_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_4437cfac ON public.event_log_entry USING btree (event_id);


--
-- Name: event_log_entry_94217c21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_94217c21 ON public.event_log_entry USING btree (event_survey_result_id);


--
-- Name: event_log_entry_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_a8452ca7 ON public.event_log_entry USING btree (person_id);


--
-- Name: event_log_entry_ce3922cc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_ce3922cc ON public.event_log_entry USING btree (global_survey_result_id);


--
-- Name: event_log_entry_d4b7764b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_d4b7764b ON public.event_log_entry USING btree (feedback_message_id);


--
-- Name: event_log_entry_e93cb7eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_e93cb7eb ON public.event_log_entry USING btree (created_by_id);


--
-- Name: event_log_entry_fde81f11; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_entry_fde81f11 ON public.event_log_entry USING btree (created_at);


--
-- Name: event_log_subscription_be324941; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_subscription_be324941 ON public.event_log_subscription USING btree (event_survey_filter_id);


--
-- Name: event_log_subscription_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_subscription_e8701ad4 ON public.event_log_subscription USING btree (user_id);


--
-- Name: event_log_subscription_entry_type_22ff4449_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_subscription_entry_type_22ff4449_idx ON public.event_log_subscription USING btree (entry_type, active);


--
-- Name: event_log_subscription_fdf6aa58; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_log_subscription_fdf6aa58 ON public.event_log_subscription USING btree (event_filter_id);


--
-- Name: feedback_feedbackmessage_4f331e2f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX feedback_feedbackmessage_4f331e2f ON public.feedback_feedbackmessage USING btree (author_id);


--
-- Name: finncon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX finncon2016_signupextra_special_diet_42414328 ON public.finncon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: finncon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX finncon2016_signupextra_special_diet_d37df680 ON public.finncon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: finncon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX finncon2018_signupextra_special_diet_42414328 ON public.finncon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: finncon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX finncon2018_signupextra_special_diet_d37df680 ON public.finncon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: frostbite2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2017_signupextra_4437cfac ON public.frostbite2017_signupextra USING btree (event_id);


--
-- Name: frostbite2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2017_signupextra_special_diet_42414328 ON public.frostbite2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: frostbite2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2017_signupextra_special_diet_d37df680 ON public.frostbite2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: frostbite2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2018_signupextra_4437cfac ON public.frostbite2018_signupextra USING btree (event_id);


--
-- Name: frostbite2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2018_signupextra_special_diet_42414328 ON public.frostbite2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: frostbite2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2018_signupextra_special_diet_d37df680 ON public.frostbite2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: frostbite2019_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2019_signupextra_4437cfac ON public.frostbite2019_signupextra USING btree (event_id);


--
-- Name: frostbite2019_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2019_signupextra_special_diet_42414328 ON public.frostbite2019_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: frostbite2019_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX frostbite2019_signupextra_special_diet_d37df680 ON public.frostbite2019_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: hitpoint2015_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hitpoint2015_signupextra_special_diet_42414328 ON public.hitpoint2015_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: hitpoint2015_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hitpoint2015_signupextra_special_diet_d37df680 ON public.hitpoint2015_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: hitpoint2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hitpoint2017_signupextra_special_diet_42414328 ON public.hitpoint2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: hitpoint2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX hitpoint2017_signupextra_special_diet_d37df680 ON public.hitpoint2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: intra_intraeventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_intraeventmeta_0a405bd6 ON public.intra_intraeventmeta USING btree (admin_group_id);


--
-- Name: intra_intraeventmeta_bb1ca3df; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_intraeventmeta_bb1ca3df ON public.intra_intraeventmeta USING btree (organizer_group_id);


--
-- Name: intra_team_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_team_0e939a4f ON public.intra_team USING btree (group_id);


--
-- Name: intra_team_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_team_4437cfac ON public.intra_team USING btree (event_id);


--
-- Name: intra_teammember_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_teammember_a8452ca7 ON public.intra_teammember USING btree (person_id);


--
-- Name: intra_teammember_f6a7ca40; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX intra_teammember_f6a7ca40 ON public.intra_teammember USING btree (team_id);


--
-- Name: kawacon2016_signupextra_needs_lodging_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2016_signupextra_needs_lodging_42414328 ON public.kawacon2016_signupextra_needs_lodging USING btree (signupextra_id);


--
-- Name: kawacon2016_signupextra_needs_lodging_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2016_signupextra_needs_lodging_a9142bf0 ON public.kawacon2016_signupextra_needs_lodging USING btree (night_id);


--
-- Name: kawacon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2016_signupextra_special_diet_42414328 ON public.kawacon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kawacon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2016_signupextra_special_diet_d37df680 ON public.kawacon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: kawacon2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_4437cfac ON public.kawacon2017_signupextra USING btree (event_id);


--
-- Name: kawacon2017_signupextra_needs_lodging_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_needs_lodging_42414328 ON public.kawacon2017_signupextra_needs_lodging USING btree (signupextra_id);


--
-- Name: kawacon2017_signupextra_needs_lodging_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_needs_lodging_a9142bf0 ON public.kawacon2017_signupextra_needs_lodging USING btree (night_id);


--
-- Name: kawacon2017_signupextra_shifts_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_shifts_42414328 ON public.kawacon2017_signupextra_shifts USING btree (signupextra_id);


--
-- Name: kawacon2017_signupextra_shifts_92547d67; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_shifts_92547d67 ON public.kawacon2017_signupextra_shifts USING btree (shift_id);


--
-- Name: kawacon2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_special_diet_42414328 ON public.kawacon2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kawacon2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kawacon2017_signupextra_special_diet_d37df680 ON public.kawacon2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: kuplii2015_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2015_signupextra_special_diet_42414328 ON public.kuplii2015_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kuplii2015_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2015_signupextra_special_diet_d37df680 ON public.kuplii2015_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: kuplii2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2016_signupextra_special_diet_42414328 ON public.kuplii2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kuplii2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2016_signupextra_special_diet_d37df680 ON public.kuplii2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: kuplii2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2017_signupextra_4437cfac ON public.kuplii2017_signupextra USING btree (event_id);


--
-- Name: kuplii2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2017_signupextra_special_diet_42414328 ON public.kuplii2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kuplii2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2017_signupextra_special_diet_d37df680 ON public.kuplii2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: kuplii2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2018_signupextra_4437cfac ON public.kuplii2018_signupextra USING btree (event_id);


--
-- Name: kuplii2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2018_signupextra_special_diet_42414328 ON public.kuplii2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: kuplii2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX kuplii2018_signupextra_special_diet_d37df680 ON public.kuplii2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: labour_alternativesignupform_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_alternativesignupform_4437cfac ON public.labour_alternativesignupform USING btree (event_id);


--
-- Name: labour_emptysignupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_emptysignupextra_4437cfac ON public.labour_emptysignupextra USING btree (event_id);


--
-- Name: labour_infolink_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_infolink_0e939a4f ON public.labour_infolink USING btree (group_id);


--
-- Name: labour_infolink_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_infolink_4437cfac ON public.labour_infolink USING btree (event_id);


--
-- Name: labour_job_7b73164c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_job_7b73164c ON public.labour_job USING btree (job_category_id);


--
-- Name: labour_jobcategory_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobcategory_4437cfac ON public.labour_jobcategory USING btree (event_id);


--
-- Name: labour_jobcategory_personnel_classes_057a1cce; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobcategory_personnel_classes_057a1cce ON public.labour_jobcategory_personnel_classes USING btree (personnelclass_id);


--
-- Name: labour_jobcategory_personnel_classes_da1e3d18; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobcategory_personnel_classes_da1e3d18 ON public.labour_jobcategory_personnel_classes USING btree (jobcategory_id);


--
-- Name: labour_jobcategory_required_qualifications_068509ea; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobcategory_required_qualifications_068509ea ON public.labour_jobcategory_required_qualifications USING btree (qualification_id);


--
-- Name: labour_jobcategory_required_qualifications_da1e3d18; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobcategory_required_qualifications_da1e3d18 ON public.labour_jobcategory_required_qualifications USING btree (jobcategory_id);


--
-- Name: labour_jobrequirement_d697ea38; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_jobrequirement_d697ea38 ON public.labour_jobrequirement USING btree (job_id);


--
-- Name: labour_laboureventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_laboureventmeta_0a405bd6 ON public.labour_laboureventmeta USING btree (admin_group_id);


--
-- Name: labour_laboureventmeta_8909846a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_laboureventmeta_8909846a ON public.labour_laboureventmeta USING btree (signup_extra_content_type_id);


--
-- Name: labour_perk_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_perk_4437cfac ON public.labour_perk USING btree (event_id);


--
-- Name: labour_personnelclass_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personnelclass_4437cfac ON public.labour_personnelclass USING btree (event_id);


--
-- Name: labour_personnelclass_event_id_fb0d1adb_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personnelclass_event_id_fb0d1adb_idx ON public.labour_personnelclass USING btree (event_id, app_label);


--
-- Name: labour_personnelclass_perks_057a1cce; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personnelclass_perks_057a1cce ON public.labour_personnelclass_perks USING btree (personnelclass_id);


--
-- Name: labour_personnelclass_perks_239a4dc4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personnelclass_perks_239a4dc4 ON public.labour_personnelclass_perks USING btree (perk_id);


--
-- Name: labour_personqualification_068509ea; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personqualification_068509ea ON public.labour_personqualification USING btree (qualification_id);


--
-- Name: labour_personqualification_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_personqualification_a8452ca7 ON public.labour_personqualification USING btree (person_id);


--
-- Name: labour_qualification_9c641fc7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_qualification_9c641fc7 ON public.labour_qualification USING btree (qualification_extra_content_type_id);


--
-- Name: labour_qualification_slug_d623f695_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_qualification_slug_d623f695_like ON public.labour_qualification USING btree (slug varchar_pattern_ops);


--
-- Name: labour_shift_cc389636; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_shift_cc389636 ON public.labour_shift USING btree (signup_id);


--
-- Name: labour_shift_d697ea38; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_shift_d697ea38 ON public.labour_shift USING btree (job_id);


--
-- Name: labour_signup_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_4437cfac ON public.labour_signup USING btree (event_id);


--
-- Name: labour_signup_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_a8452ca7 ON public.labour_signup USING btree (person_id);


--
-- Name: labour_signup_f011526f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_f011526f ON public.labour_signup USING btree (alternative_signup_form_used_id);


--
-- Name: labour_signup_job_categories_accepted_cc389636; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_accepted_cc389636 ON public.labour_signup_job_categories_accepted USING btree (signup_id);


--
-- Name: labour_signup_job_categories_accepted_da1e3d18; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_accepted_da1e3d18 ON public.labour_signup_job_categories_accepted USING btree (jobcategory_id);


--
-- Name: labour_signup_job_categories_cc389636; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_cc389636 ON public.labour_signup_job_categories USING btree (signup_id);


--
-- Name: labour_signup_job_categories_da1e3d18; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_da1e3d18 ON public.labour_signup_job_categories USING btree (jobcategory_id);


--
-- Name: labour_signup_job_categories_rejected_cc389636; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_rejected_cc389636 ON public.labour_signup_job_categories_rejected USING btree (signup_id);


--
-- Name: labour_signup_job_categories_rejected_da1e3d18; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_job_categories_rejected_da1e3d18 ON public.labour_signup_job_categories_rejected USING btree (jobcategory_id);


--
-- Name: labour_signup_personnel_classes_057a1cce; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_personnel_classes_057a1cce ON public.labour_signup_personnel_classes USING btree (personnelclass_id);


--
-- Name: labour_signup_personnel_classes_cc389636; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_signup_personnel_classes_cc389636 ON public.labour_signup_personnel_classes USING btree (signup_id);


--
-- Name: labour_survey_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_survey_4437cfac ON public.labour_survey USING btree (event_id);


--
-- Name: labour_surveyrecord_00b3bd7e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_surveyrecord_00b3bd7e ON public.labour_surveyrecord USING btree (survey_id);


--
-- Name: labour_surveyrecord_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_surveyrecord_a8452ca7 ON public.labour_surveyrecord USING btree (person_id);


--
-- Name: labour_workperiod_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX labour_workperiod_4437cfac ON public.labour_workperiod USING btree (event_id);


--
-- Name: lakeuscon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lakeuscon2016_signupextra_special_diet_42414328 ON public.lakeuscon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: lakeuscon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lakeuscon2016_signupextra_special_diet_d37df680 ON public.lakeuscon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: lippukala_code_69dfcb07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lippukala_code_69dfcb07 ON public.lippukala_code USING btree (order_id);


--
-- Name: lippukala_code_code_40127e1c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lippukala_code_code_40127e1c_like ON public.lippukala_code USING btree (code varchar_pattern_ops);


--
-- Name: lippukala_order_reference_number_222cf9ed_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX lippukala_order_reference_number_222cf9ed_like ON public.lippukala_order USING btree (reference_number varchar_pattern_ops);


--
-- Name: listings_externalevent_slug_a28283c3_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_externalevent_slug_a28283c3_like ON public.listings_externalevent USING btree (slug varchar_pattern_ops);


--
-- Name: listings_listing_events_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_listing_events_4437cfac ON public.listings_listing_events USING btree (event_id);


--
-- Name: listings_listing_events_a5acdb6c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_listing_events_a5acdb6c ON public.listings_listing_events USING btree (listing_id);


--
-- Name: listings_listing_external_events_0a829c5d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_listing_external_events_0a829c5d ON public.listings_listing_external_events USING btree (externalevent_id);


--
-- Name: listings_listing_external_events_a5acdb6c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_listing_external_events_a5acdb6c ON public.listings_listing_external_events USING btree (listing_id);


--
-- Name: listings_listing_hostname_d54965b7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX listings_listing_hostname_d54965b7_like ON public.listings_listing USING btree (hostname varchar_pattern_ops);


--
-- Name: mailings_message_8b938c66; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_message_8b938c66 ON public.mailings_message USING btree (recipient_id);


--
-- Name: mailings_personmessage_1d0adb55; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessage_1d0adb55 ON public.mailings_personmessage USING btree (body_id);


--
-- Name: mailings_personmessage_4ccaa172; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessage_4ccaa172 ON public.mailings_personmessage USING btree (message_id);


--
-- Name: mailings_personmessage_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessage_a8452ca7 ON public.mailings_personmessage USING btree (person_id);


--
-- Name: mailings_personmessage_ffaba1d1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessage_ffaba1d1 ON public.mailings_personmessage USING btree (subject_id);


--
-- Name: mailings_personmessagebody_c10f7796; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessagebody_c10f7796 ON public.mailings_personmessagebody USING btree (digest);


--
-- Name: mailings_personmessagebody_digest_3a7f7175_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessagebody_digest_3a7f7175_like ON public.mailings_personmessagebody USING btree (digest varchar_pattern_ops);


--
-- Name: mailings_personmessagesubject_c10f7796; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessagesubject_c10f7796 ON public.mailings_personmessagesubject USING btree (digest);


--
-- Name: mailings_personmessagesubject_digest_4e3a1b37_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_personmessagesubject_digest_4e3a1b37_like ON public.mailings_personmessagesubject USING btree (digest varchar_pattern_ops);


--
-- Name: mailings_recipientgroup_0e939a4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_recipientgroup_0e939a4f ON public.mailings_recipientgroup USING btree (group_id);


--
-- Name: mailings_recipientgroup_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_recipientgroup_4437cfac ON public.mailings_recipientgroup USING btree (event_id);


--
-- Name: mailings_recipientgroup_7b73164c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_recipientgroup_7b73164c ON public.mailings_recipientgroup USING btree (job_category_id);


--
-- Name: mailings_recipientgroup_a074c466; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mailings_recipientgroup_a074c466 ON public.mailings_recipientgroup USING btree (personnel_class_id);


--
-- Name: matsucon2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matsucon2018_signupextra_4437cfac ON public.matsucon2018_signupextra USING btree (event_id);


--
-- Name: matsucon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matsucon2018_signupextra_special_diet_42414328 ON public.matsucon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: matsucon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX matsucon2018_signupextra_special_diet_d37df680 ON public.matsucon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: membership_membership_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membership_26b2345e ON public.membership_membership USING btree (organization_id);


--
-- Name: membership_membership_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membership_a8452ca7 ON public.membership_membership USING btree (person_id);


--
-- Name: membership_membershipfeepayment_b5c3e75b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membershipfeepayment_b5c3e75b ON public.membership_membershipfeepayment USING btree (member_id);


--
-- Name: membership_membershipfeepayment_ba3248a2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membershipfeepayment_ba3248a2 ON public.membership_membershipfeepayment USING btree (term_id);


--
-- Name: membership_membershiporganizationmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membershiporganizationmeta_0a405bd6 ON public.membership_membershiporganizationmeta USING btree (admin_group_id);


--
-- Name: membership_membershiporganizationmeta_3c8dfdf4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_membershiporganizationmeta_3c8dfdf4 ON public.membership_membershiporganizationmeta USING btree (members_group_id);


--
-- Name: membership_term_26b2345e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX membership_term_26b2345e ON public.membership_term USING btree (organization_id);


--
-- Name: mimicon2016_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2016_signupextra_lodging_needs_42414328 ON public.mimicon2016_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: mimicon2016_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2016_signupextra_lodging_needs_a9142bf0 ON public.mimicon2016_signupextra_lodging_needs USING btree (night_id);


--
-- Name: mimicon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2016_signupextra_special_diet_42414328 ON public.mimicon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: mimicon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2016_signupextra_special_diet_d37df680 ON public.mimicon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: mimicon2018_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2018_signupextra_lodging_needs_42414328 ON public.mimicon2018_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: mimicon2018_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2018_signupextra_lodging_needs_a9142bf0 ON public.mimicon2018_signupextra_lodging_needs USING btree (night_id);


--
-- Name: mimicon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2018_signupextra_special_diet_42414328 ON public.mimicon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: mimicon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX mimicon2018_signupextra_special_diet_d37df680 ON public.mimicon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: nexmo_deliverystatusfragment_4ccaa172; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX nexmo_deliverystatusfragment_4ccaa172 ON public.nexmo_deliverystatusfragment USING btree (message_id);


--
-- Name: nippori2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX nippori2017_signupextra_4437cfac ON public.nippori2017_signupextra USING btree (event_id);


--
-- Name: oauth2_provider_accesstoken_6bc0a4eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_accesstoken_6bc0a4eb ON public.oauth2_provider_accesstoken USING btree (application_id);


--
-- Name: oauth2_provider_accesstoken_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_accesstoken_e8701ad4 ON public.oauth2_provider_accesstoken USING btree (user_id);


--
-- Name: oauth2_provider_application_9d667c2b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_application_9d667c2b ON public.oauth2_provider_application USING btree (client_secret);


--
-- Name: oauth2_provider_application_client_id_03f0cc84_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_application_client_id_03f0cc84_like ON public.oauth2_provider_application USING btree (client_id varchar_pattern_ops);


--
-- Name: oauth2_provider_application_client_secret_53133678_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_application_client_secret_53133678_like ON public.oauth2_provider_application USING btree (client_secret varchar_pattern_ops);


--
-- Name: oauth2_provider_application_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_application_e8701ad4 ON public.oauth2_provider_application USING btree (user_id);


--
-- Name: oauth2_provider_grant_6bc0a4eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_grant_6bc0a4eb ON public.oauth2_provider_grant USING btree (application_id);


--
-- Name: oauth2_provider_grant_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_grant_e8701ad4 ON public.oauth2_provider_grant USING btree (user_id);


--
-- Name: oauth2_provider_refreshtoken_6bc0a4eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_refreshtoken_6bc0a4eb ON public.oauth2_provider_refreshtoken USING btree (application_id);


--
-- Name: oauth2_provider_refreshtoken_e8701ad4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX oauth2_provider_refreshtoken_e8701ad4 ON public.oauth2_provider_refreshtoken USING btree (user_id);


--
-- Name: payments_payment_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX payments_payment_4437cfac ON public.payments_payment USING btree (event_id);


--
-- Name: payments_paymentseventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX payments_paymentseventmeta_0a405bd6 ON public.payments_paymentseventmeta USING btree (admin_group_id);


--
-- Name: popcult2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcult2017_signupextra_4437cfac ON public.popcult2017_signupextra USING btree (event_id);


--
-- Name: popcult2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcult2017_signupextra_special_diet_42414328 ON public.popcult2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: popcult2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcult2017_signupextra_special_diet_d37df680 ON public.popcult2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: popcultday2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcultday2018_signupextra_4437cfac ON public.popcultday2018_signupextra USING btree (event_id);


--
-- Name: popcultday2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcultday2018_signupextra_special_diet_42414328 ON public.popcultday2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: popcultday2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX popcultday2018_signupextra_special_diet_d37df680 ON public.popcultday2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: programme_alternativeprogrammeform_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_alternativeprogrammeform_4437cfac ON public.programme_alternativeprogrammeform USING btree (event_id);


--
-- Name: programme_category_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_category_4437cfac ON public.programme_category USING btree (event_id);


--
-- Name: programme_freeformorganizer_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_freeformorganizer_82558bcc ON public.programme_freeformorganizer USING btree (programme_id);


--
-- Name: programme_invitation_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_invitation_82558bcc ON public.programme_invitation USING btree (programme_id);


--
-- Name: programme_invitation_84566833; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_invitation_84566833 ON public.programme_invitation USING btree (role_id);


--
-- Name: programme_invitation_c6923410; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_invitation_c6923410 ON public.programme_invitation USING btree (sire_id);


--
-- Name: programme_invitation_code_88366215_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_invitation_code_88366215_like ON public.programme_invitation USING btree (code varchar_pattern_ops);


--
-- Name: programme_invitation_e93cb7eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_invitation_e93cb7eb ON public.programme_invitation USING btree (created_by_id);


--
-- Name: programme_programme_8273f993; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_8273f993 ON public.programme_programme USING btree (room_id);


--
-- Name: programme_programme_a8042b24; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_a8042b24 ON public.programme_programme USING btree (form_used_id);


--
-- Name: programme_programme_b583a629; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_b583a629 ON public.programme_programme USING btree (category_id);


--
-- Name: programme_programme_category_id_6e4de3a1_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_category_id_6e4de3a1_idx ON public.programme_programme USING btree (category_id, state);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots_0c7d745e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_hitpoint2017_preferred_time_slots_0c7d745e ON public.programme_programme_hitpoint2017_preferred_time_slots USING btree (timeslot_id);


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_hitpoint2017_preferred_time_slots_82558bcc ON public.programme_programme_hitpoint2017_preferred_time_slots USING btree (programme_id);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots_0c7d745e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_ropecon2018_preferred_time_slots_0c7d745e ON public.programme_programme_ropecon2018_preferred_time_slots USING btree (timeslot_id);


--
-- Name: programme_programme_ropecon2018_preferred_time_slots_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_ropecon2018_preferred_time_slots_82558bcc ON public.programme_programme_ropecon2018_preferred_time_slots USING btree (programme_id);


--
-- Name: programme_programme_tags_76f094bc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_tags_76f094bc ON public.programme_programme_tags USING btree (tag_id);


--
-- Name: programme_programme_tags_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programme_tags_82558bcc ON public.programme_programme_tags USING btree (programme_id);


--
-- Name: programme_programmeeventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmeeventmeta_0a405bd6 ON public.programme_programmeeventmeta USING btree (admin_group_id);


--
-- Name: programme_programmefeedback_4f331e2f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmefeedback_4f331e2f ON public.programme_programmefeedback USING btree (author_id);


--
-- Name: programme_programmefeedback_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmefeedback_82558bcc ON public.programme_programmefeedback USING btree (programme_id);


--
-- Name: programme_programmefeedback_b254ccb6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmefeedback_b254ccb6 ON public.programme_programmefeedback USING btree (hidden_by_id);


--
-- Name: programme_programmerole_06af5fcd; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmerole_06af5fcd ON public.programme_programmerole USING btree (invitation_id);


--
-- Name: programme_programmerole_82558bcc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmerole_82558bcc ON public.programme_programmerole USING btree (programme_id);


--
-- Name: programme_programmerole_84566833; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmerole_84566833 ON public.programme_programmerole USING btree (role_id);


--
-- Name: programme_programmerole_a8452ca7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_programmerole_a8452ca7 ON public.programme_programmerole USING btree (person_id);


--
-- Name: programme_role_a074c466; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_role_a074c466 ON public.programme_role USING btree (personnel_class_id);


--
-- Name: programme_room_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_room_4437cfac ON public.programme_room USING btree (event_id);


--
-- Name: programme_specialstarttime_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_specialstarttime_4437cfac ON public.programme_specialstarttime USING btree (event_id);


--
-- Name: programme_tag_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_tag_4437cfac ON public.programme_tag USING btree (event_id);


--
-- Name: programme_timeblock_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_timeblock_4437cfac ON public.programme_timeblock USING btree (event_id);


--
-- Name: programme_view_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_view_4437cfac ON public.programme_view USING btree (event_id);


--
-- Name: programme_viewroom_2e1a1398; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_viewroom_2e1a1398 ON public.programme_viewroom USING btree (view_id);


--
-- Name: programme_viewroom_8273f993; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX programme_viewroom_8273f993 ON public.programme_viewroom USING btree (room_id);


--
-- Name: ropecon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ropecon2018_signupextra_special_diet_42414328 ON public.ropecon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: ropecon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ropecon2018_signupextra_special_diet_d37df680 ON public.ropecon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: shippocon2016_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX shippocon2016_signupextra_4437cfac ON public.shippocon2016_signupextra USING btree (event_id);


--
-- Name: shippocon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX shippocon2016_signupextra_special_diet_42414328 ON public.shippocon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: shippocon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX shippocon2016_signupextra_special_diet_d37df680 ON public.shippocon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: sms_hotword_2dbcba41; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_hotword_2dbcba41 ON public.sms_hotword USING btree (slug);


--
-- Name: sms_hotword_b44cd550; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_hotword_b44cd550 ON public.sms_hotword USING btree (assigned_event_id);


--
-- Name: sms_hotword_slug_ab608568_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_hotword_slug_ab608568_like ON public.sms_hotword USING btree (slug varchar_pattern_ops);


--
-- Name: sms_nominee_category_1c5b751a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_nominee_category_1c5b751a ON public.sms_nominee_category USING btree (votecategory_id);


--
-- Name: sms_nominee_category_2e0f1201; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_nominee_category_2e0f1201 ON public.sms_nominee_category USING btree (nominee_id);


--
-- Name: sms_smseventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_smseventmeta_0a405bd6 ON public.sms_smseventmeta USING btree (admin_group_id);


--
-- Name: sms_smsmessagein_4ccaa172; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_smsmessagein_4ccaa172 ON public.sms_smsmessagein USING btree (message_id);


--
-- Name: sms_smsmessagein_e7ebb2d3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_smsmessagein_e7ebb2d3 ON public.sms_smsmessagein USING btree ("SMSEventMeta_id");


--
-- Name: sms_smsmessageout_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_smsmessageout_4437cfac ON public.sms_smsmessageout USING btree (event_id);


--
-- Name: sms_smsmessageout_97c31eab; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_smsmessageout_97c31eab ON public.sms_smsmessageout USING btree (ref_id);


--
-- Name: sms_vote_4ccaa172; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_vote_4ccaa172 ON public.sms_vote USING btree (message_id);


--
-- Name: sms_vote_b583a629; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_vote_b583a629 ON public.sms_vote USING btree (category_id);


--
-- Name: sms_vote_vote_id_229694d2_uniq; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_vote_vote_id_229694d2_uniq ON public.sms_vote USING btree (vote_id);


--
-- Name: sms_votecategory_2dbcba41; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_votecategory_2dbcba41 ON public.sms_votecategory USING btree (slug);


--
-- Name: sms_votecategory_8618c9dc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_votecategory_8618c9dc ON public.sms_votecategory USING btree (hotword_id);


--
-- Name: sms_votecategory_slug_c03fb6ca_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX sms_votecategory_slug_c03fb6ca_like ON public.sms_votecategory USING btree (slug varchar_pattern_ops);


--
-- Name: surveys_eventsurvey_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_eventsurvey_4437cfac ON public.surveys_eventsurvey USING btree (event_id);


--
-- Name: surveys_eventsurvey_5e7b1936; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_eventsurvey_5e7b1936 ON public.surveys_eventsurvey USING btree (owner_id);


--
-- Name: surveys_eventsurveyresult_00b3bd7e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_eventsurveyresult_00b3bd7e ON public.surveys_eventsurveyresult USING btree (survey_id);


--
-- Name: surveys_eventsurveyresult_4f331e2f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_eventsurveyresult_4f331e2f ON public.surveys_eventsurveyresult USING btree (author_id);


--
-- Name: surveys_globalsurvey_5e7b1936; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_globalsurvey_5e7b1936 ON public.surveys_globalsurvey USING btree (owner_id);


--
-- Name: surveys_globalsurvey_slug_f09c3896_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_globalsurvey_slug_f09c3896_like ON public.surveys_globalsurvey USING btree (slug varchar_pattern_ops);


--
-- Name: surveys_globalsurveyresult_00b3bd7e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_globalsurveyresult_00b3bd7e ON public.surveys_globalsurveyresult USING btree (survey_id);


--
-- Name: surveys_globalsurveyresult_4f331e2f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX surveys_globalsurveyresult_4f331e2f ON public.surveys_globalsurveyresult USING btree (author_id);


--
-- Name: tickets_accommodationinformation_d925f7ee; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_accommodationinformation_d925f7ee ON public.tickets_accommodationinformation USING btree (order_product_id);


--
-- Name: tickets_accommodationinformation_limit_groups_66e6cef5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_accommodationinformation_limit_groups_66e6cef5 ON public.tickets_accommodationinformation_limit_groups USING btree (accommodationinformation_id);


--
-- Name: tickets_accommodationinformation_limit_groups_db9ef8e3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_accommodationinformation_limit_groups_db9ef8e3 ON public.tickets_accommodationinformation_limit_groups USING btree (limitgroup_id);


--
-- Name: tickets_batch_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_batch_4437cfac ON public.tickets_batch USING btree (event_id);


--
-- Name: tickets_limitgroup_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_limitgroup_4437cfac ON public.tickets_limitgroup USING btree (event_id);


--
-- Name: tickets_order_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_order_4437cfac ON public.tickets_order USING btree (event_id);


--
-- Name: tickets_order_d4e60137; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_order_d4e60137 ON public.tickets_order USING btree (batch_id);


--
-- Name: tickets_orderproduct_69dfcb07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_orderproduct_69dfcb07 ON public.tickets_orderproduct USING btree (order_id);


--
-- Name: tickets_orderproduct_9bea82de; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_orderproduct_9bea82de ON public.tickets_orderproduct USING btree (product_id);


--
-- Name: tickets_product_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_product_4437cfac ON public.tickets_product USING btree (event_id);


--
-- Name: tickets_product_limit_groups_9bea82de; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_product_limit_groups_9bea82de ON public.tickets_product_limit_groups USING btree (product_id);


--
-- Name: tickets_product_limit_groups_db9ef8e3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_product_limit_groups_db9ef8e3 ON public.tickets_product_limit_groups USING btree (limitgroup_id);


--
-- Name: tickets_shirtorder_69dfcb07; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_shirtorder_69dfcb07 ON public.tickets_shirtorder USING btree (order_id);


--
-- Name: tickets_shirtorder_8222f9c0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_shirtorder_8222f9c0 ON public.tickets_shirtorder USING btree (size_id);


--
-- Name: tickets_shirtsize_94757cae; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_shirtsize_94757cae ON public.tickets_shirtsize USING btree (type_id);


--
-- Name: tickets_shirttype_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_shirttype_4437cfac ON public.tickets_shirttype USING btree (event_id);


--
-- Name: tickets_ticketseventmeta_0a405bd6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_ticketseventmeta_0a405bd6 ON public.tickets_ticketseventmeta USING btree (admin_group_id);


--
-- Name: tickets_ticketseventmeta_9fbf0b7e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tickets_ticketseventmeta_9fbf0b7e ON public.tickets_ticketseventmeta USING btree (pos_access_group_id);


--
-- Name: tracon11_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextra_lodging_needs_42414328 ON public.tracon11_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: tracon11_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextra_lodging_needs_a9142bf0 ON public.tracon11_signupextra_lodging_needs USING btree (night_id);


--
-- Name: tracon11_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextra_special_diet_42414328 ON public.tracon11_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: tracon11_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextra_special_diet_d37df680 ON public.tracon11_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: tracon11_signupextrav2_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextrav2_4437cfac ON public.tracon11_signupextrav2 USING btree (event_id);


--
-- Name: tracon11_signupextrav2_lodging_needs_328bf3a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextrav2_lodging_needs_328bf3a7 ON public.tracon11_signupextrav2_lodging_needs USING btree (signupextrav2_id);


--
-- Name: tracon11_signupextrav2_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextrav2_lodging_needs_a9142bf0 ON public.tracon11_signupextrav2_lodging_needs USING btree (night_id);


--
-- Name: tracon11_signupextrav2_special_diet_328bf3a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextrav2_special_diet_328bf3a7 ON public.tracon11_signupextrav2_special_diet USING btree (signupextrav2_id);


--
-- Name: tracon11_signupextrav2_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon11_signupextrav2_special_diet_d37df680 ON public.tracon11_signupextrav2_special_diet USING btree (specialdiet_id);


--
-- Name: tracon2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_4437cfac ON public.tracon2017_signupextra USING btree (event_id);


--
-- Name: tracon2017_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_lodging_needs_42414328 ON public.tracon2017_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: tracon2017_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_lodging_needs_a9142bf0 ON public.tracon2017_signupextra_lodging_needs USING btree (night_id);


--
-- Name: tracon2017_signupextra_pick_your_poison_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_pick_your_poison_42414328 ON public.tracon2017_signupextra_pick_your_poison USING btree (signupextra_id);


--
-- Name: tracon2017_signupextra_pick_your_poison_fee64e1f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_pick_your_poison_fee64e1f ON public.tracon2017_signupextra_pick_your_poison USING btree (poison_id);


--
-- Name: tracon2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_special_diet_42414328 ON public.tracon2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: tracon2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2017_signupextra_special_diet_d37df680 ON public.tracon2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: tracon2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_4437cfac ON public.tracon2018_signupextra USING btree (event_id);


--
-- Name: tracon2018_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_lodging_needs_42414328 ON public.tracon2018_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: tracon2018_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_lodging_needs_a9142bf0 ON public.tracon2018_signupextra_lodging_needs USING btree (night_id);


--
-- Name: tracon2018_signupextra_pick_your_poison_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_pick_your_poison_42414328 ON public.tracon2018_signupextra_pick_your_poison USING btree (signupextra_id);


--
-- Name: tracon2018_signupextra_pick_your_poison_fee64e1f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_pick_your_poison_fee64e1f ON public.tracon2018_signupextra_pick_your_poison USING btree (poison_id);


--
-- Name: tracon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_special_diet_42414328 ON public.tracon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: tracon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon2018_signupextra_special_diet_d37df680 ON public.tracon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: tracon9_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon9_signupextra_lodging_needs_42414328 ON public.tracon9_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: tracon9_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon9_signupextra_lodging_needs_a9142bf0 ON public.tracon9_signupextra_lodging_needs USING btree (night_id);


--
-- Name: tracon9_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon9_signupextra_special_diet_42414328 ON public.tracon9_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: tracon9_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tracon9_signupextra_special_diet_d37df680 ON public.tracon9_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: traconx_signupextra_lodging_needs_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX traconx_signupextra_lodging_needs_42414328 ON public.traconx_signupextra_lodging_needs USING btree (signupextra_id);


--
-- Name: traconx_signupextra_lodging_needs_a9142bf0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX traconx_signupextra_lodging_needs_a9142bf0 ON public.traconx_signupextra_lodging_needs USING btree (night_id);


--
-- Name: traconx_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX traconx_signupextra_special_diet_42414328 ON public.traconx_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: traconx_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX traconx_signupextra_special_diet_d37df680 ON public.traconx_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: tylycon2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tylycon2017_signupextra_4437cfac ON public.tylycon2017_signupextra USING btree (event_id);


--
-- Name: tylycon2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tylycon2017_signupextra_special_diet_42414328 ON public.tylycon2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: tylycon2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX tylycon2017_signupextra_special_diet_d37df680 ON public.tylycon2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: worldcon75_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX worldcon75_signupextra_4437cfac ON public.worldcon75_signupextra USING btree (event_id);


--
-- Name: worldcon75_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX worldcon75_signupextra_special_diet_42414328 ON public.worldcon75_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: worldcon75_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX worldcon75_signupextra_special_diet_d37df680 ON public.worldcon75_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: yukicon2016_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2016_signupextra_special_diet_42414328 ON public.yukicon2016_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: yukicon2016_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2016_signupextra_special_diet_d37df680 ON public.yukicon2016_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: yukicon2017_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2017_signupextra_4437cfac ON public.yukicon2017_signupextra USING btree (event_id);


--
-- Name: yukicon2017_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2017_signupextra_special_diet_42414328 ON public.yukicon2017_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: yukicon2017_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2017_signupextra_special_diet_d37df680 ON public.yukicon2017_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: yukicon2017_signupextra_work_days_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2017_signupextra_work_days_42414328 ON public.yukicon2017_signupextra_work_days USING btree (signupextra_id);


--
-- Name: yukicon2017_signupextra_work_days_99bcb875; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2017_signupextra_work_days_99bcb875 ON public.yukicon2017_signupextra_work_days USING btree (eventday_id);


--
-- Name: yukicon2018_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2018_signupextra_4437cfac ON public.yukicon2018_signupextra USING btree (event_id);


--
-- Name: yukicon2018_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2018_signupextra_special_diet_42414328 ON public.yukicon2018_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: yukicon2018_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2018_signupextra_special_diet_d37df680 ON public.yukicon2018_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: yukicon2018_signupextra_work_days_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2018_signupextra_work_days_42414328 ON public.yukicon2018_signupextra_work_days USING btree (signupextra_id);


--
-- Name: yukicon2018_signupextra_work_days_99bcb875; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2018_signupextra_work_days_99bcb875 ON public.yukicon2018_signupextra_work_days USING btree (eventday_id);


--
-- Name: yukicon2019_signupextra_4437cfac; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2019_signupextra_4437cfac ON public.yukicon2019_signupextra USING btree (event_id);


--
-- Name: yukicon2019_signupextra_special_diet_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2019_signupextra_special_diet_42414328 ON public.yukicon2019_signupextra_special_diet USING btree (signupextra_id);


--
-- Name: yukicon2019_signupextra_special_diet_d37df680; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2019_signupextra_special_diet_d37df680 ON public.yukicon2019_signupextra_special_diet USING btree (specialdiet_id);


--
-- Name: yukicon2019_signupextra_work_days_42414328; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2019_signupextra_work_days_42414328 ON public.yukicon2019_signupextra_work_days USING btree (signupextra_id);


--
-- Name: yukicon2019_signupextra_work_days_99bcb875; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX yukicon2019_signupextra_work_days_99bcb875 ON public.yukicon2019_signupextra_work_days USING btree (eventday_id);


--
-- Name: labour_laboureventmeta D0c45c90c899f282a1abfffd2f7f77f8; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_laboureventmeta
    ADD CONSTRAINT "D0c45c90c899f282a1abfffd2f7f77f8" FOREIGN KEY (signup_extra_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_qualification D0f16bf4a839240c70d8b1eee5b3779f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_qualification
    ADD CONSTRAINT "D0f16bf4a839240c70d8b1eee5b3779f" FOREIGN KEY (qualification_extra_content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry D105895583fb84ebcf3b48b9b647b376; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT "D105895583fb84ebcf3b48b9b647b376" FOREIGN KEY (event_survey_result_id) REFERENCES public.surveys_eventsurveyresult(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry D464671a7fd2ba5a5303e1a203243997; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT "D464671a7fd2ba5a5303e1a203243997" FOREIGN KEY (global_survey_result_id) REFERENCES public.surveys_globalsurveyresult(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup D4970224b4c616c5e8f24faf0cdf2b41; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup
    ADD CONSTRAINT "D4970224b4c616c5e8f24faf0cdf2b41" FOREIGN KEY (alternative_signup_form_used_id) REFERENCES public.labour_alternativesignupform(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_accommodationinformation_limit_groups D7e9d6eac83eb1d24cc3e29661aa71a9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation_limit_groups
    ADD CONSTRAINT "D7e9d6eac83eb1d24cc3e29661aa71a9" FOREIGN KEY (accommodationinformation_id) REFERENCES public.tickets_accommodationinformation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_common_qualifications_jvkortti D8a89871f53bc1af42a785ec2a8b778e; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_common_qualifications_jvkortti
    ADD CONSTRAINT "D8a89871f53bc1af42a785ec2a8b778e" FOREIGN KEY (personqualification_id) REFERENCES public.labour_personqualification(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2016_signupextra_special_diet a_signupextra_id_0e3d250b_fk_animecon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_special_diet
    ADD CONSTRAINT a_signupextra_id_0e3d250b_fk_animecon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.animecon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2016_signupextra_lodging_needs a_signupextra_id_0fe70a98_fk_animecon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_lodging_needs
    ADD CONSTRAINT a_signupextra_id_0fe70a98_fk_animecon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.animecon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2015_signupextra_lodging_needs a_signupextra_id_3e5bfb35_fk_animecon2015_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_lodging_needs
    ADD CONSTRAINT a_signupextra_id_3e5bfb35_fk_animecon2015_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.animecon2015_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2015_signupextra_special_diet a_signupextra_id_4083b445_fk_animecon2015_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_special_diet
    ADD CONSTRAINT a_signupextra_id_4083b445_fk_animecon2015_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.animecon2015_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_smtpserver_domains acce_emailaliasdomain_id_725c76a4_fk_access_emailaliasdomain_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver_domains
    ADD CONSTRAINT acce_emailaliasdomain_id_725c76a4_fk_access_emailaliasdomain_id FOREIGN KEY (emailaliasdomain_id) REFERENCES public.access_emailaliasdomain(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailalias acces_group_grant_id_2a432527_fk_access_groupemailaliasgrant_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT acces_group_grant_id_2a432527_fk_access_groupemailaliasgrant_id FOREIGN KEY (group_grant_id) REFERENCES public.access_groupemailaliasgrant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_accessorganizationmeta access_accesso_organization_id_6fd5296f_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_accessorganizationmeta
    ADD CONSTRAINT access_accesso_organization_id_6fd5296f_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_accessorganizationmeta access_accessorganizat_admin_group_id_fba465cc_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_accessorganizationmeta
    ADD CONSTRAINT access_accessorganizat_admin_group_id_fba465cc_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailalias access_emailal_domain_id_1c715651_fk_access_emailaliasdomain_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT access_emailal_domain_id_1c715651_fk_access_emailaliasdomain_id FOREIGN KEY (domain_id) REFERENCES public.access_emailaliasdomain(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailaliastype access_emailal_domain_id_384f9e33_fk_access_emailaliasdomain_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliastype
    ADD CONSTRAINT access_emailal_domain_id_384f9e33_fk_access_emailaliasdomain_id FOREIGN KEY (domain_id) REFERENCES public.access_emailaliasdomain(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailaliasdomain access_emailal_organization_id_5bc3eedd_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailaliasdomain
    ADD CONSTRAINT access_emailal_organization_id_5bc3eedd_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailalias access_emailalias_person_id_d36631ab_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT access_emailalias_person_id_d36631ab_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_emailalias access_emailalias_type_id_707106ba_fk_access_emailaliastype_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_emailalias
    ADD CONSTRAINT access_emailalias_type_id_707106ba_fk_access_emailaliastype_id FOREIGN KEY (type_id) REFERENCES public.access_emailaliastype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_grantedprivilege access_grantedpriv_privilege_id_6da68281_fk_access_privilege_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_grantedprivilege
    ADD CONSTRAINT access_grantedpriv_privilege_id_6da68281_fk_access_privilege_id FOREIGN KEY (privilege_id) REFERENCES public.access_privilege(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_grantedprivilege access_grantedprivilege_person_id_f05c5d84_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_grantedprivilege
    ADD CONSTRAINT access_grantedprivilege_person_id_f05c5d84_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_groupemailaliasgrant access_groupemaila_type_id_9bc02ef3_fk_access_emailaliastype_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupemailaliasgrant
    ADD CONSTRAINT access_groupemaila_type_id_9bc02ef3_fk_access_emailaliastype_id FOREIGN KEY (type_id) REFERENCES public.access_emailaliastype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_groupemailaliasgrant access_groupemailaliasgrant_group_id_00052328_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupemailaliasgrant
    ADD CONSTRAINT access_groupemailaliasgrant_group_id_00052328_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_groupprivilege access_groupprivil_privilege_id_036ee3bc_fk_access_privilege_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege
    ADD CONSTRAINT access_groupprivil_privilege_id_036ee3bc_fk_access_privilege_id FOREIGN KEY (privilege_id) REFERENCES public.access_privilege(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_groupprivilege access_groupprivilege_event_id_b0b63a87_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege
    ADD CONSTRAINT access_groupprivilege_event_id_b0b63a87_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_groupprivilege access_groupprivilege_group_id_5bdb3244_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_groupprivilege
    ADD CONSTRAINT access_groupprivilege_group_id_5bdb3244_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_internalemailalias access_interna_domain_id_ab77b615_fk_access_emailaliasdomain_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_internalemailalias
    ADD CONSTRAINT access_interna_domain_id_ab77b615_fk_access_emailaliasdomain_id FOREIGN KEY (domain_id) REFERENCES public.access_emailaliasdomain(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_internalemailalias access_internalemailalias_event_id_67f9e0dd_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_internalemailalias
    ADD CONSTRAINT access_internalemailalias_event_id_67f9e0dd_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_slackaccess access_slackaccess_privilege_id_d6089b77_fk_access_privilege_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_slackaccess
    ADD CONSTRAINT access_slackaccess_privilege_id_d6089b77_fk_access_privilege_id FOREIGN KEY (privilege_id) REFERENCES public.access_privilege(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_smtppassword access_smtppass_smtp_server_id_1fbe2a7a_fk_access_smtpserver_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtppassword
    ADD CONSTRAINT access_smtppass_smtp_server_id_1fbe2a7a_fk_access_smtpserver_id FOREIGN KEY (smtp_server_id) REFERENCES public.access_smtpserver(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_smtppassword access_smtppassword_person_id_89672f1a_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtppassword
    ADD CONSTRAINT access_smtppassword_person_id_89672f1a_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: access_smtpserver_domains access_smtpserve_smtpserver_id_6baacdcb_fk_access_smtpserver_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.access_smtpserver_domains
    ADD CONSTRAINT access_smtpserve_smtpserver_id_6baacdcb_fk_access_smtpserver_id FOREIGN KEY (smtpserver_id) REFERENCES public.access_smtpserver(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2016_signupextra_special_diet aico_signupextra_id_bbc49f9a_fk_aicon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra_special_diet
    ADD CONSTRAINT aico_signupextra_id_bbc49f9a_fk_aicon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.aicon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2018_signupextra_special_diet aico_signupextra_id_f36245c4_fk_aicon2018_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra_special_diet
    ADD CONSTRAINT aico_signupextra_id_f36245c4_fk_aicon2018_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.aicon2018_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2016_signupextra_special_diet aicon2016_s_specialdiet_id_7979648c_fk_aicon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra_special_diet
    ADD CONSTRAINT aicon2016_s_specialdiet_id_7979648c_fk_aicon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.aicon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2016_signupextra aicon2016_signupextra_signup_id_24462d43_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2016_signupextra
    ADD CONSTRAINT aicon2016_signupextra_signup_id_24462d43_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2018_signupextra_special_diet aicon2018_s_specialdiet_id_37f75c77_fk_aicon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra_special_diet
    ADD CONSTRAINT aicon2018_s_specialdiet_id_37f75c77_fk_aicon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.aicon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: aicon2018_signupextra aicon2018_signupextra_signup_id_fe0ef4d2_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.aicon2018_signupextra
    ADD CONSTRAINT aicon2018_signupextra_signup_id_fe0ef4d2_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2015_signupextra_lodging_needs animecon2015_signupe_night_id_ce59630a_fk_animecon2015_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_lodging_needs
    ADD CONSTRAINT animecon2015_signupe_night_id_ce59630a_fk_animecon2015_night_id FOREIGN KEY (night_id) REFERENCES public.animecon2015_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2015_signupextra animecon2015_signupextra_signup_id_5e198a46_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra
    ADD CONSTRAINT animecon2015_signupextra_signup_id_5e198a46_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2016_signupextra_lodging_needs animecon2016_signupe_night_id_bc88d453_fk_animecon2016_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_lodging_needs
    ADD CONSTRAINT animecon2016_signupe_night_id_bc88d453_fk_animecon2016_night_id FOREIGN KEY (night_id) REFERENCES public.animecon2016_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2016_signupextra animecon2016_signupextra_signup_id_b7b76e70_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra
    ADD CONSTRAINT animecon2016_signupextra_signup_id_b7b76e70_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2016_signupextra_special_diet animecon_specialdiet_id_11b4f192_fk_animecon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2016_signupextra_special_diet
    ADD CONSTRAINT animecon_specialdiet_id_11b4f192_fk_animecon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.animecon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: animecon2015_signupextra_special_diet animecon_specialdiet_id_a4c9e66b_fk_animecon2015_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.animecon2015_signupextra_special_diet
    ADD CONSTRAINT animecon_specialdiet_id_a4c9e66b_fk_animecon2015_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.animecon2015_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permiss_permission_id_84c5c92e_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permiss_content_type_id_2f476e4b_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_per_permission_id_1fbb5f2c_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_batch badges__personnel_class_id_271df0ef_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_batch
    ADD CONSTRAINT badges__personnel_class_id_271df0ef_fk_labour_personnelclass_id FOREIGN KEY (personnel_class_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badge badges__personnel_class_id_9e440435_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges__personnel_class_id_9e440435_fk_labour_personnelclass_id FOREIGN KEY (personnel_class_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badge badges_badge_batch_id_9f1ce5b1_fk_badges_batch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges_badge_batch_id_9f1ce5b1_fk_badges_batch_id FOREIGN KEY (batch_id) REFERENCES public.badges_batch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badge badges_badge_created_by_id_c5ff2ddb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges_badge_created_by_id_c5ff2ddb_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badge badges_badge_person_id_4cca74fd_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges_badge_person_id_4cca74fd_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badge badges_badge_revoked_by_id_b6962e71_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badge
    ADD CONSTRAINT badges_badge_revoked_by_id_b6962e71_fk_auth_user_id FOREIGN KEY (revoked_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badgeseventmeta badges_badgeseventmeta_admin_group_id_fc8c43c8_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badgeseventmeta
    ADD CONSTRAINT badges_badgeseventmeta_admin_group_id_fc8c43c8_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_badgeseventmeta badges_badgeseventmeta_event_id_34d22bf5_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_badgeseventmeta
    ADD CONSTRAINT badges_badgeseventmeta_event_id_34d22bf5_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: badges_batch badges_batch_event_id_4587b0d6_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.badges_batch
    ADD CONSTRAINT badges_batch_event_id_4587b0d6_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_emailverificationtoken core_emailverificationtoke_person_id_e0aada72_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_emailverificationtoken
    ADD CONSTRAINT core_emailverificationtoke_person_id_e0aada72_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_event core_event_organization_id_a2ce68e9_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_organization_id_a2ce68e9_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_event core_event_venue_id_d74b5c9b_fk_core_venue_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_event
    ADD CONSTRAINT core_event_venue_id_d74b5c9b_fk_core_venue_id FOREIGN KEY (venue_id) REFERENCES public.core_venue(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_passwordresettoken core_passwordresettoken_person_id_0b8e45c0_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_passwordresettoken
    ADD CONSTRAINT core_passwordresettoken_person_id_0b8e45c0_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: core_person core_person_user_id_3dfe5fcf_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.core_person
    ADD CONSTRAINT core_person_user_id_3dfe5fcf_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextra_special_diet de_signupextra_id_0ce3578c_fk_desucon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra_special_diet
    ADD CONSTRAINT de_signupextra_id_0ce3578c_fk_desucon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.desucon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextrav2_special_diet desuc_signupextrav2_id_a1f10bc4_fk_desucon2016_signupextrav2_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2_special_diet
    ADD CONSTRAINT desuc_signupextrav2_id_a1f10bc4_fk_desucon2016_signupextrav2_id FOREIGN KEY (signupextrav2_id) REFERENCES public.desucon2016_signupextrav2(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextra desucon2016_signupextra_signup_id_883b05a4_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra
    ADD CONSTRAINT desucon2016_signupextra_signup_id_883b05a4_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextrav2 desucon2016_signupextrav2_event_id_ee6f4c01_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2
    ADD CONSTRAINT desucon2016_signupextrav2_event_id_ee6f4c01_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextrav2 desucon2016_signupextrav2_person_id_29c53c5d_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2
    ADD CONSTRAINT desucon2016_signupextrav2_person_id_29c53c5d_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2017_signupextra desucon2017_signupextra_event_id_c6ec463c_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra
    ADD CONSTRAINT desucon2017_signupextra_event_id_c6ec463c_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2017_signupextra desucon2017_signupextra_person_id_6c671a8f_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra
    ADD CONSTRAINT desucon2017_signupextra_person_id_6c671a8f_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2018_signupextra desucon2018_signupextra_event_id_71deb19e_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra
    ADD CONSTRAINT desucon2018_signupextra_event_id_71deb19e_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2018_signupextra desucon2018_signupextra_person_id_d51e39cb_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra
    ADD CONSTRAINT desucon2018_signupextra_person_id_d51e39cb_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2019_signupextra desucon2019_signupextra_event_id_03f1eecc_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra
    ADD CONSTRAINT desucon2019_signupextra_event_id_03f1eecc_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2019_signupextra desucon2019_signupextra_person_id_930ca7c4_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra
    ADD CONSTRAINT desucon2019_signupextra_person_id_930ca7c4_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2017_signupextra_special_diet desucon20_signupextra_id_12848af8_fk_desucon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra_special_diet
    ADD CONSTRAINT desucon20_signupextra_id_12848af8_fk_desucon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.desucon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2019_signupextra_special_diet desucon20_signupextra_id_192fcfc8_fk_desucon2019_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra_special_diet
    ADD CONSTRAINT desucon20_signupextra_id_192fcfc8_fk_desucon2019_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.desucon2019_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2018_signupextra_special_diet desucon20_signupextra_id_faeb796d_fk_desucon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra_special_diet
    ADD CONSTRAINT desucon20_signupextra_id_faeb796d_fk_desucon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.desucon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2017_signupextra_special_diet desucon20_specialdiet_id_1320d296_fk_desucon2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2017_signupextra_special_diet
    ADD CONSTRAINT desucon20_specialdiet_id_1320d296_fk_desucon2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.desucon2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2019_signupextra_special_diet desucon20_specialdiet_id_6e6bd350_fk_desucon2019_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2019_signupextra_special_diet
    ADD CONSTRAINT desucon20_specialdiet_id_6e6bd350_fk_desucon2019_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.desucon2019_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextrav2_special_diet desucon20_specialdiet_id_8b334325_fk_desucon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextrav2_special_diet
    ADD CONSTRAINT desucon20_specialdiet_id_8b334325_fk_desucon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.desucon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2018_signupextra_special_diet desucon20_specialdiet_id_99b90e97_fk_desucon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2018_signupextra_special_diet
    ADD CONSTRAINT desucon20_specialdiet_id_99b90e97_fk_desucon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.desucon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desucon2016_signupextra_special_diet desucon20_specialdiet_id_f2a2eb01_fk_desucon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desucon2016_signupextra_special_diet
    ADD CONSTRAINT desucon20_specialdiet_id_f2a2eb01_fk_desucon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.desucon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desuprofile_integration_confirmationcode desuprofile_integration_co_person_id_30adca39_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_confirmationcode
    ADD CONSTRAINT desuprofile_integration_co_person_id_30adca39_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: desuprofile_integration_connection desuprofile_integration_connec_user_id_fb8f4d2c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.desuprofile_integration_connection
    ADD CONSTRAINT desuprofile_integration_connec_user_id_fb8f4d2c_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: directory_directoryorganizationmeta directory_dire_organization_id_50be5a38_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryorganizationmeta
    ADD CONSTRAINT directory_dire_organization_id_50be5a38_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: directory_directoryaccessgroup directory_dire_organization_id_fbf7e185_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryaccessgroup
    ADD CONSTRAINT directory_dire_organization_id_fbf7e185_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: directory_directoryaccessgroup directory_directoryaccessgro_group_id_54b04030_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.directory_directoryaccessgroup
    ADD CONSTRAINT directory_directoryaccessgro_group_id_54b04030_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_content_type_id_c4bce8eb_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_content_type_id_c4bce8eb_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment_concon_parts enrollment_e_conconpart_id_a31ad2d9_fk_enrollment_conconpart_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_concon_parts
    ADD CONSTRAINT enrollment_e_conconpart_id_a31ad2d9_fk_enrollment_conconpart_id FOREIGN KEY (conconpart_id) REFERENCES public.enrollment_conconpart(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment_special_diet enrollment_e_enrollment_id_24d0a686_fk_enrollment_enrollment_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_special_diet
    ADD CONSTRAINT enrollment_e_enrollment_id_24d0a686_fk_enrollment_enrollment_id FOREIGN KEY (enrollment_id) REFERENCES public.enrollment_enrollment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment_concon_parts enrollment_e_enrollment_id_db71f2cb_fk_enrollment_enrollment_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_concon_parts
    ADD CONSTRAINT enrollment_e_enrollment_id_db71f2cb_fk_enrollment_enrollment_id FOREIGN KEY (enrollment_id) REFERENCES public.enrollment_enrollment(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment enrollment_enrollment_event_id_688bf29a_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment
    ADD CONSTRAINT enrollment_enrollment_event_id_688bf29a_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment enrollment_enrollment_person_id_7567f500_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment
    ADD CONSTRAINT enrollment_enrollment_person_id_7567f500_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollmenteventmeta enrollment_enrollmente_admin_group_id_36dd0d32_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollmenteventmeta
    ADD CONSTRAINT enrollment_enrollmente_admin_group_id_36dd0d32_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollmenteventmeta enrollment_enrollmenteventme_event_id_34b90512_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollmenteventmeta
    ADD CONSTRAINT enrollment_enrollmenteventme_event_id_34b90512_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: enrollment_enrollment_special_diet enrollment_specialdiet_id_0bd4c253_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.enrollment_enrollment_special_diet
    ADD CONSTRAINT enrollment_specialdiet_id_0bd4c253_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry eve_feedback_message_id_3acc7090_fk_feedback_feedbackmessage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT eve_feedback_message_id_3acc7090_fk_feedback_feedbackmessage_id FOREIGN KEY (feedback_message_id) REFERENCES public.feedback_feedbackmessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_subscription event_event_survey_filter_id_7cb834e7_fk_surveys_eventsurvey_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_subscription
    ADD CONSTRAINT event_event_survey_filter_id_7cb834e7_fk_surveys_eventsurvey_id FOREIGN KEY (event_survey_filter_id) REFERENCES public.surveys_eventsurvey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry event_log_entr_organization_id_cd93d7fb_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT event_log_entr_organization_id_cd93d7fb_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry event_log_entry_created_by_id_355ad5a2_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT event_log_entry_created_by_id_355ad5a2_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry event_log_entry_event_id_f13a35d2_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT event_log_entry_event_id_f13a35d2_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_entry event_log_entry_person_id_b043f99f_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_entry
    ADD CONSTRAINT event_log_entry_person_id_b043f99f_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_subscription event_log_subscriptio_event_filter_id_dc05b2ac_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_subscription
    ADD CONSTRAINT event_log_subscriptio_event_filter_id_dc05b2ac_fk_core_event_id FOREIGN KEY (event_filter_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: event_log_subscription event_log_subscription_user_id_bc3b7408_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_log_subscription
    ADD CONSTRAINT event_log_subscription_user_id_bc3b7408_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: feedback_feedbackmessage feedback_feedbackmessage_author_id_1530360c_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.feedback_feedbackmessage
    ADD CONSTRAINT feedback_feedbackmessage_author_id_1530360c_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2016_signupextra_special_diet fi_signupextra_id_25fed210_fk_finncon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra_special_diet
    ADD CONSTRAINT fi_signupextra_id_25fed210_fk_finncon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.finncon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2018_signupextra_special_diet fi_signupextra_id_a5d3567c_fk_finncon2018_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra_special_diet
    ADD CONSTRAINT fi_signupextra_id_a5d3567c_fk_finncon2018_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.finncon2018_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2016_signupextra finncon2016_signupextra_signup_id_a2aadeeb_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra
    ADD CONSTRAINT finncon2016_signupextra_signup_id_a2aadeeb_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2018_signupextra finncon2018_signupextra_signup_id_1b0e61d0_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra
    ADD CONSTRAINT finncon2018_signupextra_signup_id_1b0e61d0_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2016_signupextra_special_diet finncon20_specialdiet_id_85c394f6_fk_finncon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2016_signupextra_special_diet
    ADD CONSTRAINT finncon20_specialdiet_id_85c394f6_fk_finncon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.finncon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: finncon2018_signupextra_special_diet finncon20_specialdiet_id_8ec42076_fk_finncon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.finncon2018_signupextra_special_diet
    ADD CONSTRAINT finncon20_specialdiet_id_8ec42076_fk_finncon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.finncon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme form_used_id_e35c2164_fk_programme_alternativeprogrammeform_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme
    ADD CONSTRAINT form_used_id_e35c2164_fk_programme_alternativeprogrammeform_id FOREIGN KEY (form_used_id) REFERENCES public.programme_alternativeprogrammeform(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2017_signupextra_special_diet frostbi_signupextra_id_102c791a_fk_frostbite2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra_special_diet
    ADD CONSTRAINT frostbi_signupextra_id_102c791a_fk_frostbite2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.frostbite2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2018_signupextra_special_diet frostbi_signupextra_id_7fdfee8b_fk_frostbite2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra_special_diet
    ADD CONSTRAINT frostbi_signupextra_id_7fdfee8b_fk_frostbite2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.frostbite2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2019_signupextra_special_diet frostbi_signupextra_id_814e535d_fk_frostbite2019_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra_special_diet
    ADD CONSTRAINT frostbi_signupextra_id_814e535d_fk_frostbite2019_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.frostbite2019_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2019_signupextra_special_diet frostbi_specialdiet_id_4372a87f_fk_frostbite2019_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra_special_diet
    ADD CONSTRAINT frostbi_specialdiet_id_4372a87f_fk_frostbite2019_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.frostbite2019_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2017_signupextra_special_diet frostbi_specialdiet_id_d1a5df15_fk_frostbite2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra_special_diet
    ADD CONSTRAINT frostbi_specialdiet_id_d1a5df15_fk_frostbite2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.frostbite2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2018_signupextra_special_diet frostbi_specialdiet_id_d22ebe8f_fk_frostbite2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra_special_diet
    ADD CONSTRAINT frostbi_specialdiet_id_d22ebe8f_fk_frostbite2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.frostbite2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2016_signupextra frostbite2016_signupextr_signup_id_492cfdb1_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2016_signupextra
    ADD CONSTRAINT frostbite2016_signupextr_signup_id_492cfdb1_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2017_signupextra frostbite2017_signupextra_event_id_c5b1f437_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra
    ADD CONSTRAINT frostbite2017_signupextra_event_id_c5b1f437_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2017_signupextra frostbite2017_signupextra_person_id_13d02157_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2017_signupextra
    ADD CONSTRAINT frostbite2017_signupextra_person_id_13d02157_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2018_signupextra frostbite2018_signupextra_event_id_29a7e18c_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra
    ADD CONSTRAINT frostbite2018_signupextra_event_id_29a7e18c_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2018_signupextra frostbite2018_signupextra_person_id_1962eecb_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2018_signupextra
    ADD CONSTRAINT frostbite2018_signupextra_person_id_1962eecb_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2019_signupextra frostbite2019_signupextra_event_id_4d866055_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra
    ADD CONSTRAINT frostbite2019_signupextra_event_id_4d866055_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: frostbite2019_signupextra frostbite2019_signupextra_person_id_a1115537_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.frostbite2019_signupextra
    ADD CONSTRAINT frostbite2019_signupextra_person_id_a1115537_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2017_signupextra_special_diet h_signupextra_id_15a2675c_fk_hitpoint2017_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra_special_diet
    ADD CONSTRAINT h_signupextra_id_15a2675c_fk_hitpoint2017_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.hitpoint2017_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2015_signupextra_special_diet h_signupextra_id_85886027_fk_hitpoint2015_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra_special_diet
    ADD CONSTRAINT h_signupextra_id_85886027_fk_hitpoint2015_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.hitpoint2015_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2015_signupextra hitpoint2015_signupextra_signup_id_4026d4fb_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra
    ADD CONSTRAINT hitpoint2015_signupextra_signup_id_4026d4fb_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2017_signupextra hitpoint2017_signupextra_signup_id_5e03e712_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra
    ADD CONSTRAINT hitpoint2017_signupextra_signup_id_5e03e712_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2015_signupextra_special_diet hitpoint_specialdiet_id_6f6b2ec6_fk_hitpoint2015_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2015_signupextra_special_diet
    ADD CONSTRAINT hitpoint_specialdiet_id_6f6b2ec6_fk_hitpoint2015_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.hitpoint2015_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: hitpoint2017_signupextra_special_diet hitpoint_specialdiet_id_78103888_fk_hitpoint2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hitpoint2017_signupextra_special_diet
    ADD CONSTRAINT hitpoint_specialdiet_id_78103888_fk_hitpoint2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.hitpoint2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_intraeventmeta intra_intraeventme_organizer_group_id_fe100965_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_intraeventmeta
    ADD CONSTRAINT intra_intraeventme_organizer_group_id_fe100965_fk_auth_group_id FOREIGN KEY (organizer_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_intraeventmeta intra_intraeventmeta_admin_group_id_0fb9c0b0_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_intraeventmeta
    ADD CONSTRAINT intra_intraeventmeta_admin_group_id_0fb9c0b0_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_intraeventmeta intra_intraeventmeta_event_id_86c9bde2_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_intraeventmeta
    ADD CONSTRAINT intra_intraeventmeta_event_id_86c9bde2_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_team intra_team_event_id_b801aca9_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_team
    ADD CONSTRAINT intra_team_event_id_b801aca9_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_team intra_team_group_id_9dce430d_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_team
    ADD CONSTRAINT intra_team_group_id_9dce430d_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_teammember intra_teammember_person_id_d1a2a240_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_teammember
    ADD CONSTRAINT intra_teammember_person_id_d1a2a240_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: intra_teammember intra_teammember_team_id_c9f4d093_fk_intra_team_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.intra_teammember
    ADD CONSTRAINT intra_teammember_team_id_c9f4d093_fk_intra_team_id FOREIGN KEY (team_id) REFERENCES public.intra_team(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2016_signupextra_special_diet ka_signupextra_id_52caee97_fk_kawacon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_special_diet
    ADD CONSTRAINT ka_signupextra_id_52caee97_fk_kawacon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.kawacon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2016_signupextra_needs_lodging ka_signupextra_id_5cccff99_fk_kawacon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_needs_lodging
    ADD CONSTRAINT ka_signupextra_id_5cccff99_fk_kawacon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.kawacon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2016_signupextra_needs_lodging kawacon2016_signupext_night_id_10fd96bc_fk_kawacon2016_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2016_signupext_night_id_10fd96bc_fk_kawacon2016_night_id FOREIGN KEY (night_id) REFERENCES public.kawacon2016_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2016_signupextra kawacon2016_signupextra_signup_id_b5902ba5_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra
    ADD CONSTRAINT kawacon2016_signupextra_signup_id_b5902ba5_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_needs_lodging kawacon2017_signupext_night_id_9a1c44be_fk_kawacon2017_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_needs_lodging
    ADD CONSTRAINT kawacon2017_signupext_night_id_9a1c44be_fk_kawacon2017_night_id FOREIGN KEY (night_id) REFERENCES public.kawacon2017_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_shifts kawacon2017_signupext_shift_id_51a1fcc5_fk_kawacon2017_shift_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_shifts
    ADD CONSTRAINT kawacon2017_signupext_shift_id_51a1fcc5_fk_kawacon2017_shift_id FOREIGN KEY (shift_id) REFERENCES public.kawacon2017_shift(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra kawacon2017_signupextra_event_id_781dd815_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra
    ADD CONSTRAINT kawacon2017_signupextra_event_id_781dd815_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra kawacon2017_signupextra_person_id_2b2304ea_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra
    ADD CONSTRAINT kawacon2017_signupextra_person_id_2b2304ea_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_shifts kawacon20_signupextra_id_a58d9288_fk_kawacon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_shifts
    ADD CONSTRAINT kawacon20_signupextra_id_a58d9288_fk_kawacon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.kawacon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_special_diet kawacon20_signupextra_id_c4077076_fk_kawacon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_special_diet
    ADD CONSTRAINT kawacon20_signupextra_id_c4077076_fk_kawacon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.kawacon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_needs_lodging kawacon20_signupextra_id_c9348470_fk_kawacon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_needs_lodging
    ADD CONSTRAINT kawacon20_signupextra_id_c9348470_fk_kawacon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.kawacon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2017_signupextra_special_diet kawacon20_specialdiet_id_0bd8cd33_fk_kawacon2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2017_signupextra_special_diet
    ADD CONSTRAINT kawacon20_specialdiet_id_0bd8cd33_fk_kawacon2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kawacon2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kawacon2016_signupextra_special_diet kawacon20_specialdiet_id_806c9b63_fk_kawacon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kawacon2016_signupextra_special_diet
    ADD CONSTRAINT kawacon20_specialdiet_id_806c9b63_fk_kawacon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kawacon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2016_signupextra_special_diet kup_signupextra_id_40d17874_fk_kuplii2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra_special_diet
    ADD CONSTRAINT kup_signupextra_id_40d17874_fk_kuplii2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.kuplii2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2015_signupextra_special_diet kup_signupextra_id_9529574b_fk_kuplii2015_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra_special_diet
    ADD CONSTRAINT kup_signupextra_id_9529574b_fk_kuplii2015_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.kuplii2015_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2015_signupextra kuplii2015_signupextra_signup_id_1bffcfdb_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra
    ADD CONSTRAINT kuplii2015_signupextra_signup_id_1bffcfdb_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2015_signupextra_special_diet kuplii2015_specialdiet_id_5b4e8659_fk_kuplii2015_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2015_signupextra_special_diet
    ADD CONSTRAINT kuplii2015_specialdiet_id_5b4e8659_fk_kuplii2015_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kuplii2015_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2016_signupextra kuplii2016_signupextra_signup_id_8896f075_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra
    ADD CONSTRAINT kuplii2016_signupextra_signup_id_8896f075_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2016_signupextra_special_diet kuplii2016_specialdiet_id_053c34ec_fk_kuplii2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2016_signupextra_special_diet
    ADD CONSTRAINT kuplii2016_specialdiet_id_053c34ec_fk_kuplii2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kuplii2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2017_signupextra kuplii2017_signupextra_event_id_a142d95d_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra
    ADD CONSTRAINT kuplii2017_signupextra_event_id_a142d95d_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2017_signupextra_special_diet kuplii2017_signupextra_id_a922b21a_fk_kuplii2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra_special_diet
    ADD CONSTRAINT kuplii2017_signupextra_id_a922b21a_fk_kuplii2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.kuplii2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2017_signupextra kuplii2017_signupextra_person_id_b9148d52_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra
    ADD CONSTRAINT kuplii2017_signupextra_person_id_b9148d52_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2017_signupextra_special_diet kuplii2017_specialdiet_id_ffb41e30_fk_kuplii2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2017_signupextra_special_diet
    ADD CONSTRAINT kuplii2017_specialdiet_id_ffb41e30_fk_kuplii2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kuplii2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2018_signupextra kuplii2018_signupextra_event_id_ff454760_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra
    ADD CONSTRAINT kuplii2018_signupextra_event_id_ff454760_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2018_signupextra_special_diet kuplii2018_signupextra_id_4233b02a_fk_kuplii2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra_special_diet
    ADD CONSTRAINT kuplii2018_signupextra_id_4233b02a_fk_kuplii2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.kuplii2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2018_signupextra kuplii2018_signupextra_person_id_e53a0420_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra
    ADD CONSTRAINT kuplii2018_signupextra_person_id_e53a0420_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: kuplii2018_signupextra_special_diet kuplii2018_specialdiet_id_7f3d25a5_fk_kuplii2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.kuplii2018_signupextra_special_diet
    ADD CONSTRAINT kuplii2018_specialdiet_id_7f3d25a5_fk_kuplii2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.kuplii2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_alternativesignupform labour_alternativesignupform_event_id_8bbc0126_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_alternativesignupform
    ADD CONSTRAINT labour_alternativesignupform_event_id_8bbc0126_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_emptysignupextra labour_emptysignupextra_event_id_a13b5c89_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_emptysignupextra
    ADD CONSTRAINT labour_emptysignupextra_event_id_a13b5c89_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_emptysignupextra labour_emptysignupextra_person_id_1927c3e9_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_emptysignupextra
    ADD CONSTRAINT labour_emptysignupextra_person_id_1927c3e9_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_obsoleteemptysignupextrav1 labour_emptysignupextra_signup_id_f1ae244c_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_obsoleteemptysignupextrav1
    ADD CONSTRAINT labour_emptysignupextra_signup_id_f1ae244c_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_infolink labour_infolink_event_id_d38b6e45_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_infolink
    ADD CONSTRAINT labour_infolink_event_id_d38b6e45_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_infolink labour_infolink_group_id_4311e349_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_infolink
    ADD CONSTRAINT labour_infolink_group_id_4311e349_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobcategory_personnel_classes labour_j_personnelclass_id_ff76a774_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_personnel_classes
    ADD CONSTRAINT labour_j_personnelclass_id_ff76a774_fk_labour_personnelclass_id FOREIGN KEY (personnelclass_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_job labour_job_job_category_id_9d70afde_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_job
    ADD CONSTRAINT labour_job_job_category_id_9d70afde_fk_labour_jobcategory_id FOREIGN KEY (job_category_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobcategory_required_qualifications labour_job_qualification_id_61392645_fk_labour_qualification_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_required_qualifications
    ADD CONSTRAINT labour_job_qualification_id_61392645_fk_labour_qualification_id FOREIGN KEY (qualification_id) REFERENCES public.labour_qualification(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobcategory_required_qualifications labour_jobcate_jobcategory_id_3cb328a5_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_required_qualifications
    ADD CONSTRAINT labour_jobcate_jobcategory_id_3cb328a5_fk_labour_jobcategory_id FOREIGN KEY (jobcategory_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobcategory_personnel_classes labour_jobcate_jobcategory_id_55756148_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory_personnel_classes
    ADD CONSTRAINT labour_jobcate_jobcategory_id_55756148_fk_labour_jobcategory_id FOREIGN KEY (jobcategory_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobcategory labour_jobcategory_event_id_1e21d50d_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobcategory
    ADD CONSTRAINT labour_jobcategory_event_id_1e21d50d_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_jobrequirement labour_jobrequirement_job_id_61d80756_fk_labour_job_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_jobrequirement
    ADD CONSTRAINT labour_jobrequirement_job_id_61d80756_fk_labour_job_id FOREIGN KEY (job_id) REFERENCES public.labour_job(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_laboureventmeta labour_laboureventmeta_admin_group_id_f9241604_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_laboureventmeta
    ADD CONSTRAINT labour_laboureventmeta_admin_group_id_f9241604_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_laboureventmeta labour_laboureventmeta_event_id_fb48ee26_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_laboureventmeta
    ADD CONSTRAINT labour_laboureventmeta_event_id_fb48ee26_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_personnelclass_perks labour_p_personnelclass_id_5db1c6e8_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass_perks
    ADD CONSTRAINT labour_p_personnelclass_id_5db1c6e8_fk_labour_personnelclass_id FOREIGN KEY (personnelclass_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_personqualification labour_per_qualification_id_4c308ec9_fk_labour_qualification_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personqualification
    ADD CONSTRAINT labour_per_qualification_id_4c308ec9_fk_labour_qualification_id FOREIGN KEY (qualification_id) REFERENCES public.labour_qualification(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_perk labour_perk_event_id_2a97e683_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_perk
    ADD CONSTRAINT labour_perk_event_id_2a97e683_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_personnelclass labour_personnelclass_event_id_b0317718_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass
    ADD CONSTRAINT labour_personnelclass_event_id_b0317718_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_personnelclass_perks labour_personnelclass_perks_perk_id_e028f3cf_fk_labour_perk_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personnelclass_perks
    ADD CONSTRAINT labour_personnelclass_perks_perk_id_e028f3cf_fk_labour_perk_id FOREIGN KEY (perk_id) REFERENCES public.labour_perk(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_personqualification labour_personqualification_person_id_f4bae3e1_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_personqualification
    ADD CONSTRAINT labour_personqualification_person_id_f4bae3e1_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_personnel_classes labour_s_personnelclass_id_e1f04525_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_personnel_classes
    ADD CONSTRAINT labour_s_personnelclass_id_e1f04525_fk_labour_personnelclass_id FOREIGN KEY (personnelclass_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_shift labour_shift_job_id_36dd099c_fk_labour_job_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_shift
    ADD CONSTRAINT labour_shift_job_id_36dd099c_fk_labour_job_id FOREIGN KEY (job_id) REFERENCES public.labour_job(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_shift labour_shift_signup_id_030cb7ae_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_shift
    ADD CONSTRAINT labour_shift_signup_id_030cb7ae_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories_accepted labour_signup__jobcategory_id_9ae81fa7_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_accepted
    ADD CONSTRAINT labour_signup__jobcategory_id_9ae81fa7_fk_labour_jobcategory_id FOREIGN KEY (jobcategory_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories labour_signup__jobcategory_id_b447c4bb_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories
    ADD CONSTRAINT labour_signup__jobcategory_id_b447c4bb_fk_labour_jobcategory_id FOREIGN KEY (jobcategory_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories_rejected labour_signup__jobcategory_id_df04007f_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_rejected
    ADD CONSTRAINT labour_signup__jobcategory_id_df04007f_fk_labour_jobcategory_id FOREIGN KEY (jobcategory_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup labour_signup_event_id_e5a1f121_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup
    ADD CONSTRAINT labour_signup_event_id_e5a1f121_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories labour_signup_job_catego_signup_id_215bc17f_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories
    ADD CONSTRAINT labour_signup_job_catego_signup_id_215bc17f_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories_rejected labour_signup_job_catego_signup_id_aea2a80d_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_rejected
    ADD CONSTRAINT labour_signup_job_catego_signup_id_aea2a80d_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_job_categories_accepted labour_signup_job_catego_signup_id_b8987e0e_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_job_categories_accepted
    ADD CONSTRAINT labour_signup_job_catego_signup_id_b8987e0e_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup labour_signup_person_id_69459f4c_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup
    ADD CONSTRAINT labour_signup_person_id_69459f4c_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_signup_personnel_classes labour_signup_personnel__signup_id_3a45091a_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_signup_personnel_classes
    ADD CONSTRAINT labour_signup_personnel__signup_id_3a45091a_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_survey labour_survey_event_id_47fe14bb_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_survey
    ADD CONSTRAINT labour_survey_event_id_47fe14bb_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_surveyrecord labour_surveyrecord_person_id_796a7ef7_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_surveyrecord
    ADD CONSTRAINT labour_surveyrecord_person_id_796a7ef7_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_surveyrecord labour_surveyrecord_survey_id_7c57d742_fk_labour_survey_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_surveyrecord
    ADD CONSTRAINT labour_surveyrecord_survey_id_7c57d742_fk_labour_survey_id FOREIGN KEY (survey_id) REFERENCES public.labour_survey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: labour_workperiod labour_workperiod_event_id_59f25286_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.labour_workperiod
    ADD CONSTRAINT labour_workperiod_event_id_59f25286_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lakeuscon2016_signupextra_special_diet lakeusc_specialdiet_id_337e8423_fk_lakeuscon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra_special_diet
    ADD CONSTRAINT lakeusc_specialdiet_id_337e8423_fk_lakeuscon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.lakeuscon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lakeuscon2016_signupextra lakeuscon2016_signupextr_signup_id_5747105f_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra
    ADD CONSTRAINT lakeuscon2016_signupextr_signup_id_5747105f_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lippukala_code lippukala_code_order_id_919a620c_fk_lippukala_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lippukala_code
    ADD CONSTRAINT lippukala_code_order_id_919a620c_fk_lippukala_order_id FOREIGN KEY (order_id) REFERENCES public.lippukala_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: listings_listing_external_events listings_externalevent_id_779259ec_fk_listings_externalevent_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_external_events
    ADD CONSTRAINT listings_externalevent_id_779259ec_fk_listings_externalevent_id FOREIGN KEY (externalevent_id) REFERENCES public.listings_externalevent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: listings_listing_events listings_listing_eve_listing_id_82df5bb7_fk_listings_listing_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_events
    ADD CONSTRAINT listings_listing_eve_listing_id_82df5bb7_fk_listings_listing_id FOREIGN KEY (listing_id) REFERENCES public.listings_listing(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: listings_listing_events listings_listing_events_event_id_797e1061_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_events
    ADD CONSTRAINT listings_listing_events_event_id_797e1061_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: listings_listing_external_events listings_listing_ext_listing_id_771c58ae_fk_listings_listing_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.listings_listing_external_events
    ADD CONSTRAINT listings_listing_ext_listing_id_771c58ae_fk_listings_listing_id FOREIGN KEY (listing_id) REFERENCES public.listings_listing(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_recipientgroup mailing_personnel_class_id_de97b3f1_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup
    ADD CONSTRAINT mailing_personnel_class_id_de97b3f1_fk_labour_personnelclass_id FOREIGN KEY (personnel_class_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_personmessage mailing_subject_id_3e0f05a7_fk_mailings_personmessagesubject_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage
    ADD CONSTRAINT mailing_subject_id_3e0f05a7_fk_mailings_personmessagesubject_id FOREIGN KEY (subject_id) REFERENCES public.mailings_personmessagesubject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_message mailings_me_recipient_id_ce463be1_fk_mailings_recipientgroup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_message
    ADD CONSTRAINT mailings_me_recipient_id_ce463be1_fk_mailings_recipientgroup_id FOREIGN KEY (recipient_id) REFERENCES public.mailings_recipientgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_personmessage mailings_pers_body_id_f7af2c8e_fk_mailings_personmessagebody_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage
    ADD CONSTRAINT mailings_pers_body_id_f7af2c8e_fk_mailings_personmessagebody_id FOREIGN KEY (body_id) REFERENCES public.mailings_personmessagebody(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_personmessage mailings_personmessa_message_id_71cb79ef_fk_mailings_message_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage
    ADD CONSTRAINT mailings_personmessa_message_id_71cb79ef_fk_mailings_message_id FOREIGN KEY (message_id) REFERENCES public.mailings_message(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_personmessage mailings_personmessage_person_id_05b8f64d_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_personmessage
    ADD CONSTRAINT mailings_personmessage_person_id_05b8f64d_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_recipientgroup mailings_reci_job_category_id_13d2489b_fk_labour_jobcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup
    ADD CONSTRAINT mailings_reci_job_category_id_13d2489b_fk_labour_jobcategory_id FOREIGN KEY (job_category_id) REFERENCES public.labour_jobcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_recipientgroup mailings_recipientgroup_event_id_bf96d4fb_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup
    ADD CONSTRAINT mailings_recipientgroup_event_id_bf96d4fb_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mailings_recipientgroup mailings_recipientgroup_group_id_9ff711ef_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mailings_recipientgroup
    ADD CONSTRAINT mailings_recipientgroup_group_id_9ff711ef_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matsucon2018_signupextra matsucon2018_signupextra_event_id_6481be7c_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra
    ADD CONSTRAINT matsucon2018_signupextra_event_id_6481be7c_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matsucon2018_signupextra matsucon2018_signupextra_person_id_928283e8_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra
    ADD CONSTRAINT matsucon2018_signupextra_person_id_928283e8_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matsucon2018_signupextra_special_diet matsucon20_specialdiet_id_11d3e283_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra_special_diet
    ADD CONSTRAINT matsucon20_specialdiet_id_11d3e283_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: matsucon2018_signupextra_special_diet matsucon_signupextra_id_01671a50_fk_matsucon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.matsucon2018_signupextra_special_diet
    ADD CONSTRAINT matsucon_signupextra_id_01671a50_fk_matsucon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.matsucon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membershiporganizationmeta membership_mem_organization_id_1b2daa7e_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershiporganizationmeta
    ADD CONSTRAINT membership_mem_organization_id_1b2daa7e_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membership membership_mem_organization_id_a3fda0eb_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membership
    ADD CONSTRAINT membership_mem_organization_id_a3fda0eb_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membershipfeepayment membership_membe_member_id_4bba2660_fk_membership_membership_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershipfeepayment
    ADD CONSTRAINT membership_membe_member_id_4bba2660_fk_membership_membership_id FOREIGN KEY (member_id) REFERENCES public.membership_membership(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membershiporganizationmeta membership_membershi_members_group_id_53cc2b3e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershiporganizationmeta
    ADD CONSTRAINT membership_membershi_members_group_id_53cc2b3e_fk_auth_group_id FOREIGN KEY (members_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membership membership_membership_person_id_4593a1f9_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membership
    ADD CONSTRAINT membership_membership_person_id_4593a1f9_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membershipfeepayment membership_membershipfee_term_id_5936abef_fk_membership_term_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershipfeepayment
    ADD CONSTRAINT membership_membershipfee_term_id_5936abef_fk_membership_term_id FOREIGN KEY (term_id) REFERENCES public.membership_term(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_membershiporganizationmeta membership_membershipo_admin_group_id_a43faffa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_membershiporganizationmeta
    ADD CONSTRAINT membership_membershipo_admin_group_id_a43faffa_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: membership_term membership_ter_organization_id_2856c581_fk_core_organization_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.membership_term
    ADD CONSTRAINT membership_ter_organization_id_2856c581_fk_core_organization_id FOREIGN KEY (organization_id) REFERENCES public.core_organization(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2018_signupextra_special_diet mi_signupextra_id_747da6c5_fk_mimicon2018_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_special_diet
    ADD CONSTRAINT mi_signupextra_id_747da6c5_fk_mimicon2018_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.mimicon2018_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2016_signupextra_lodging_needs mi_signupextra_id_dadaf58c_fk_mimicon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_lodging_needs
    ADD CONSTRAINT mi_signupextra_id_dadaf58c_fk_mimicon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.mimicon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2016_signupextra_special_diet mi_signupextra_id_e577e3ae_fk_mimicon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_special_diet
    ADD CONSTRAINT mi_signupextra_id_e577e3ae_fk_mimicon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.mimicon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2018_signupextra_lodging_needs mi_signupextra_id_f2fb2e3b_fk_mimicon2018_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_lodging_needs
    ADD CONSTRAINT mi_signupextra_id_f2fb2e3b_fk_mimicon2018_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.mimicon2018_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2016_signupextra_lodging_needs mimicon2016_signupext_night_id_a72b6b12_fk_mimicon2016_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2016_signupext_night_id_a72b6b12_fk_mimicon2016_night_id FOREIGN KEY (night_id) REFERENCES public.mimicon2016_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2016_signupextra mimicon2016_signupextra_signup_id_59c09464_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra
    ADD CONSTRAINT mimicon2016_signupextra_signup_id_59c09464_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2018_signupextra_lodging_needs mimicon2018_signupext_night_id_542962c3_fk_mimicon2018_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_lodging_needs
    ADD CONSTRAINT mimicon2018_signupext_night_id_542962c3_fk_mimicon2018_night_id FOREIGN KEY (night_id) REFERENCES public.mimicon2018_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2018_signupextra mimicon2018_signupextra_signup_id_6676d73f_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra
    ADD CONSTRAINT mimicon2018_signupextra_signup_id_6676d73f_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2016_signupextra_special_diet mimicon20_specialdiet_id_2cab16d8_fk_mimicon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2016_signupextra_special_diet
    ADD CONSTRAINT mimicon20_specialdiet_id_2cab16d8_fk_mimicon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.mimicon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: mimicon2018_signupextra_special_diet mimicon20_specialdiet_id_cf5ce9d8_fk_mimicon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.mimicon2018_signupextra_special_diet
    ADD CONSTRAINT mimicon20_specialdiet_id_cf5ce9d8_fk_mimicon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.mimicon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: nexmo_deliverystatusfragment nexmo_deliverys_message_id_87b65c24_fk_nexmo_outboundmessage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nexmo_deliverystatusfragment
    ADD CONSTRAINT nexmo_deliverys_message_id_87b65c24_fk_nexmo_outboundmessage_id FOREIGN KEY (message_id) REFERENCES public.nexmo_outboundmessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: nippori2017_signupextra nippori2017_signupextra_event_id_7c6fe68c_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nippori2017_signupextra
    ADD CONSTRAINT nippori2017_signupextra_event_id_7c6fe68c_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: nippori2017_signupextra nippori2017_signupextra_person_id_d78ca762_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nippori2017_signupextra
    ADD CONSTRAINT nippori2017_signupextra_person_id_d78ca762_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oaut_access_token_id_775e84e8_fk_oauth2_provider_accesstoken_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oaut_access_token_id_775e84e8_fk_oauth2_provider_accesstoken_id FOREIGN KEY (access_token_id) REFERENCES public.oauth2_provider_accesstoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_user_id_6e4c9a65_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth2_provider_accesstoken_user_id_6e4c9a65_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_application oauth2_provider_application_user_id_79829054_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_application
    ADD CONSTRAINT oauth2_provider_application_user_id_79829054_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth2_provider_grant_user_id_e8f62af8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth2_provider_grant_user_id_e8f62af8_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_user_id_da837fce_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth2_provider_refreshtoken_user_id_da837fce_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth_application_id_2d1c311b_fk_oauth2_provider_application_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_refreshtoken
    ADD CONSTRAINT oauth_application_id_2d1c311b_fk_oauth2_provider_application_id FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth_application_id_81923564_fk_oauth2_provider_application_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_grant
    ADD CONSTRAINT oauth_application_id_81923564_fk_oauth2_provider_application_id FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth_application_id_b22886e1_fk_oauth2_provider_application_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.oauth2_provider_accesstoken
    ADD CONSTRAINT oauth_application_id_b22886e1_fk_oauth2_provider_application_id FOREIGN KEY (application_id) REFERENCES public.oauth2_provider_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_payment payments_payment_event_id_1aa1e2db_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_payment
    ADD CONSTRAINT payments_payment_event_id_1aa1e2db_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_paymentseventmeta payments_paymentsevent_admin_group_id_eabdf94c_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_paymentseventmeta
    ADD CONSTRAINT payments_paymentsevent_admin_group_id_eabdf94c_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: payments_paymentseventmeta payments_paymentseventmeta_event_id_945aaefa_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payments_paymentseventmeta
    ADD CONSTRAINT payments_paymentseventmeta_event_id_945aaefa_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcultday2018_signupextra_special_diet popcul_signupextra_id_b22a9f3e_fk_popcultday2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra_special_diet
    ADD CONSTRAINT popcul_signupextra_id_b22a9f3e_fk_popcultday2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.popcultday2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcult2017_signupextra popcult2017_signupextra_event_id_5d295723_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra
    ADD CONSTRAINT popcult2017_signupextra_event_id_5d295723_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcult2017_signupextra popcult2017_signupextra_person_id_a6b1ea92_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra
    ADD CONSTRAINT popcult2017_signupextra_person_id_a6b1ea92_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcult2017_signupextra_special_diet popcult201_specialdiet_id_21cca6aa_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra_special_diet
    ADD CONSTRAINT popcult201_specialdiet_id_21cca6aa_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcult2017_signupextra_special_diet popcult20_signupextra_id_65c246da_fk_popcult2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcult2017_signupextra_special_diet
    ADD CONSTRAINT popcult20_signupextra_id_65c246da_fk_popcult2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.popcult2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcultday2018_signupextra popcultday2018_signupextra_event_id_f40fc210_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra
    ADD CONSTRAINT popcultday2018_signupextra_event_id_f40fc210_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcultday2018_signupextra popcultday2018_signupextra_person_id_91b7c764_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra
    ADD CONSTRAINT popcultday2018_signupextra_person_id_91b7c764_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: popcultday2018_signupextra_special_diet popcultday_specialdiet_id_f4e89a43_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.popcultday2018_signupextra_special_diet
    ADD CONSTRAINT popcultday_specialdiet_id_f4e89a43_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_role program_personnel_class_id_80cd2894_fk_labour_personnelclass_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_role
    ADD CONSTRAINT program_personnel_class_id_80cd2894_fk_labour_personnelclass_id FOREIGN KEY (personnel_class_id) REFERENCES public.labour_personnelclass(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_alternativeprogrammeform programme_alternativeprogram_event_id_8c2c8d29_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_alternativeprogrammeform
    ADD CONSTRAINT programme_alternativeprogram_event_id_8c2c8d29_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_category programme_category_event_id_543f9962_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_category
    ADD CONSTRAINT programme_category_event_id_543f9962_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_freeformorganizer programme_freef_programme_id_6b52860d_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_freeformorganizer
    ADD CONSTRAINT programme_freef_programme_id_6b52860d_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_invitation programme_invit_programme_id_aa6cf384_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invit_programme_id_aa6cf384_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_invitation programme_invita_sire_id_bba296f0_fk_programme_programmerole_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invita_sire_id_bba296f0_fk_programme_programmerole_id FOREIGN KEY (sire_id) REFERENCES public.programme_programmerole(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_invitation programme_invitation_created_by_id_c12b2d9b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invitation_created_by_id_c12b2d9b_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_invitation programme_invitation_role_id_d52adb64_fk_programme_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_invitation
    ADD CONSTRAINT programme_invitation_role_id_d52adb64_fk_programme_role_id FOREIGN KEY (role_id) REFERENCES public.programme_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmerole programme_pro_invitation_id_b7973069_fk_programme_invitation_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole
    ADD CONSTRAINT programme_pro_invitation_id_b7973069_fk_programme_invitation_id FOREIGN KEY (invitation_id) REFERENCES public.programme_invitation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots programme_prog_timeslot_id_badea01c_fk_hitpoint2017_timeslot_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_hitpoint2017_preferred_time_slots
    ADD CONSTRAINT programme_prog_timeslot_id_badea01c_fk_hitpoint2017_timeslot_id FOREIGN KEY (timeslot_id) REFERENCES public.hitpoint2017_timeslot(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_ropecon2018_preferred_time_slots programme_progr_programme_id_1fbb5c78_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_ropecon2018_preferred_time_slots
    ADD CONSTRAINT programme_progr_programme_id_1fbb5c78_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_tags programme_progr_programme_id_5f486c08_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_tags
    ADD CONSTRAINT programme_progr_programme_id_5f486c08_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmefeedback programme_progr_programme_id_8c29e8df_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmefeedback
    ADD CONSTRAINT programme_progr_programme_id_8c29e8df_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmerole programme_progr_programme_id_aa452c66_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole
    ADD CONSTRAINT programme_progr_programme_id_aa452c66_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_hitpoint2017_preferred_time_slots programme_progr_programme_id_d1293657_fk_programme_programme_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_hitpoint2017_preferred_time_slots
    ADD CONSTRAINT programme_progr_programme_id_d1293657_fk_programme_programme_id FOREIGN KEY (programme_id) REFERENCES public.programme_programme(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_ropecon2018_preferred_time_slots programme_progr_timeslot_id_c54a73c2_fk_ropecon2018_timeslot_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_ropecon2018_preferred_time_slots
    ADD CONSTRAINT programme_progr_timeslot_id_c54a73c2_fk_ropecon2018_timeslot_id FOREIGN KEY (timeslot_id) REFERENCES public.ropecon2018_timeslot(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme programme_program_category_id_915d2622_fk_programme_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme
    ADD CONSTRAINT programme_program_category_id_915d2622_fk_programme_category_id FOREIGN KEY (category_id) REFERENCES public.programme_category(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme programme_programme_room_id_94b7fc9d_fk_programme_room_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme
    ADD CONSTRAINT programme_programme_room_id_94b7fc9d_fk_programme_room_id FOREIGN KEY (room_id) REFERENCES public.programme_room(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programme_tags programme_programme_tags_tag_id_d1f12a82_fk_programme_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programme_tags
    ADD CONSTRAINT programme_programme_tags_tag_id_d1f12a82_fk_programme_tag_id FOREIGN KEY (tag_id) REFERENCES public.programme_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmeeventmeta programme_programmeeve_admin_group_id_cb2cc13e_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmeeventmeta
    ADD CONSTRAINT programme_programmeeve_admin_group_id_cb2cc13e_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmeeventmeta programme_programmeeventmeta_event_id_5511f336_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmeeventmeta
    ADD CONSTRAINT programme_programmeeventmeta_event_id_5511f336_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmefeedback programme_programmefeedba_hidden_by_id_ab5e0d9f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmefeedback
    ADD CONSTRAINT programme_programmefeedba_hidden_by_id_ab5e0d9f_fk_auth_user_id FOREIGN KEY (hidden_by_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmefeedback programme_programmefeedbac_author_id_2b02e587_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmefeedback
    ADD CONSTRAINT programme_programmefeedbac_author_id_2b02e587_fk_core_person_id FOREIGN KEY (author_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmerole programme_programmerole_person_id_c6c414c6_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole
    ADD CONSTRAINT programme_programmerole_person_id_c6c414c6_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_programmerole programme_programmerole_role_id_435e73a8_fk_programme_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_programmerole
    ADD CONSTRAINT programme_programmerole_role_id_435e73a8_fk_programme_role_id FOREIGN KEY (role_id) REFERENCES public.programme_role(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_room programme_room_event_id_7c662e2b_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_room
    ADD CONSTRAINT programme_room_event_id_7c662e2b_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_specialstarttime programme_specialstarttime_event_id_7b426c03_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_specialstarttime
    ADD CONSTRAINT programme_specialstarttime_event_id_7b426c03_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_tag programme_tag_event_id_6b7447e6_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_tag
    ADD CONSTRAINT programme_tag_event_id_6b7447e6_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_timeblock programme_timeblock_event_id_4c100d3e_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_timeblock
    ADD CONSTRAINT programme_timeblock_event_id_4c100d3e_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_view programme_view_event_id_691e64f3_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_view
    ADD CONSTRAINT programme_view_event_id_691e64f3_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_viewroom programme_viewroom_room_id_cb646402_fk_programme_room_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_viewroom
    ADD CONSTRAINT programme_viewroom_room_id_cb646402_fk_programme_room_id FOREIGN KEY (room_id) REFERENCES public.programme_room(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: programme_viewroom programme_viewroom_view_id_8d22905f_fk_programme_view_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.programme_viewroom
    ADD CONSTRAINT programme_viewroom_view_id_8d22905f_fk_programme_view_id FOREIGN KEY (view_id) REFERENCES public.programme_view(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ropecon2018_signupextra_special_diet ro_signupextra_id_489ca226_fk_ropecon2018_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra_special_diet
    ADD CONSTRAINT ro_signupextra_id_489ca226_fk_ropecon2018_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.ropecon2018_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ropecon2018_signupextra ropecon2018_signupextra_signup_id_762d5b34_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra
    ADD CONSTRAINT ropecon2018_signupextra_signup_id_762d5b34_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ropecon2018_signupextra_special_diet ropecon20_specialdiet_id_1363fc97_fk_ropecon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ropecon2018_signupextra_special_diet
    ADD CONSTRAINT ropecon20_specialdiet_id_1363fc97_fk_ropecon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.ropecon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shippocon2016_signupextra_special_diet shippoc_signupextra_id_b29d6fba_fk_shippocon2016_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra_special_diet
    ADD CONSTRAINT shippoc_signupextra_id_b29d6fba_fk_shippocon2016_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.shippocon2016_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shippocon2016_signupextra_special_diet shippoc_specialdiet_id_19f63b56_fk_shippocon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra_special_diet
    ADD CONSTRAINT shippoc_specialdiet_id_19f63b56_fk_shippocon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.shippocon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shippocon2016_signupextra shippocon2016_signupextra_event_id_4479ba8d_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra
    ADD CONSTRAINT shippocon2016_signupextra_event_id_4479ba8d_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: shippocon2016_signupextra shippocon2016_signupextra_person_id_19fe9525_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shippocon2016_signupextra
    ADD CONSTRAINT shippocon2016_signupextra_person_id_19fe9525_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: lakeuscon2016_signupextra_special_diet signupextra_id_3cb66b20_fk_lakeuscon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lakeuscon2016_signupextra_special_diet
    ADD CONSTRAINT signupextra_id_3cb66b20_fk_lakeuscon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.lakeuscon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_hotword sms_hotword_assigned_event_id_d298f898_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_hotword
    ADD CONSTRAINT sms_hotword_assigned_event_id_d298f898_fk_core_event_id FOREIGN KEY (assigned_event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_nominee_category sms_nominee_cat_votecategory_id_08bc1fec_fk_sms_votecategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee_category
    ADD CONSTRAINT sms_nominee_cat_votecategory_id_08bc1fec_fk_sms_votecategory_id FOREIGN KEY (votecategory_id) REFERENCES public.sms_votecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_nominee_category sms_nominee_category_nominee_id_a2874e71_fk_sms_nominee_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_nominee_category
    ADD CONSTRAINT sms_nominee_category_nominee_id_a2874e71_fk_sms_nominee_id FOREIGN KEY (nominee_id) REFERENCES public.sms_nominee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smseventmeta sms_smseventmeta_admin_group_id_4524f722_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smseventmeta
    ADD CONSTRAINT sms_smseventmeta_admin_group_id_4524f722_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smseventmeta sms_smseventmeta_event_id_2ff17584_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smseventmeta
    ADD CONSTRAINT sms_smseventmeta_event_id_2ff17584_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smsmessagein sms_smsme_SMSEventMeta_id_a1385f58_fk_sms_smseventmeta_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessagein
    ADD CONSTRAINT "sms_smsme_SMSEventMeta_id_a1385f58_fk_sms_smseventmeta_event_id" FOREIGN KEY ("SMSEventMeta_id") REFERENCES public.sms_smseventmeta(event_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smsmessagein sms_smsmessagein_message_id_03b4453b_fk_nexmo_inboundmessage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessagein
    ADD CONSTRAINT sms_smsmessagein_message_id_03b4453b_fk_nexmo_inboundmessage_id FOREIGN KEY (message_id) REFERENCES public.nexmo_inboundmessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smsmessageout sms_smsmessageou_event_id_992ac8cf_fk_sms_smseventmeta_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessageout
    ADD CONSTRAINT sms_smsmessageou_event_id_992ac8cf_fk_sms_smseventmeta_event_id FOREIGN KEY (event_id) REFERENCES public.sms_smseventmeta(event_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_smsmessageout sms_smsmessageout_ref_id_76a283ed_fk_nexmo_outboundmessage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_smsmessageout
    ADD CONSTRAINT sms_smsmessageout_ref_id_76a283ed_fk_nexmo_outboundmessage_id FOREIGN KEY (ref_id) REFERENCES public.nexmo_outboundmessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_vote sms_vote_category_id_c14fe76a_fk_sms_votecategory_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_vote
    ADD CONSTRAINT sms_vote_category_id_c14fe76a_fk_sms_votecategory_id FOREIGN KEY (category_id) REFERENCES public.sms_votecategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_vote sms_vote_message_id_90333d83_fk_nexmo_inboundmessage_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_vote
    ADD CONSTRAINT sms_vote_message_id_90333d83_fk_nexmo_inboundmessage_id FOREIGN KEY (message_id) REFERENCES public.nexmo_inboundmessage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_vote sms_vote_vote_id_229694d2_fk_sms_nominee_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_vote
    ADD CONSTRAINT sms_vote_vote_id_229694d2_fk_sms_nominee_id FOREIGN KEY (vote_id) REFERENCES public.sms_nominee(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sms_votecategory sms_votecategory_hotword_id_a37cf6c3_fk_sms_hotword_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sms_votecategory
    ADD CONSTRAINT sms_votecategory_hotword_id_a37cf6c3_fk_sms_hotword_id FOREIGN KEY (hotword_id) REFERENCES public.sms_hotword(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_eventsurveyresult surveys_eventsurve_survey_id_446992bc_fk_surveys_eventsurvey_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurveyresult
    ADD CONSTRAINT surveys_eventsurve_survey_id_446992bc_fk_surveys_eventsurvey_id FOREIGN KEY (survey_id) REFERENCES public.surveys_eventsurvey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_eventsurvey surveys_eventsurvey_event_id_d6a821a9_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurvey
    ADD CONSTRAINT surveys_eventsurvey_event_id_d6a821a9_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_eventsurvey surveys_eventsurvey_owner_id_dc65d2af_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurvey
    ADD CONSTRAINT surveys_eventsurvey_owner_id_dc65d2af_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_eventsurveyresult surveys_eventsurveyresult_author_id_1d35eb67_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_eventsurveyresult
    ADD CONSTRAINT surveys_eventsurveyresult_author_id_1d35eb67_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_globalsurveyresult surveys_globalsur_survey_id_b613a23a_fk_surveys_globalsurvey_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurveyresult
    ADD CONSTRAINT surveys_globalsur_survey_id_b613a23a_fk_surveys_globalsurvey_id FOREIGN KEY (survey_id) REFERENCES public.surveys_globalsurvey(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_globalsurvey surveys_globalsurvey_owner_id_66f1ec62_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurvey
    ADD CONSTRAINT surveys_globalsurvey_owner_id_66f1ec62_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: surveys_globalsurveyresult surveys_globalsurveyresult_author_id_862ef18f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.surveys_globalsurveyresult
    ADD CONSTRAINT surveys_globalsurveyresult_author_id_862ef18f_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_accommodationinformation tickets_ac_order_product_id_5eb3a6ae_fk_tickets_orderproduct_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation
    ADD CONSTRAINT tickets_ac_order_product_id_5eb3a6ae_fk_tickets_orderproduct_id FOREIGN KEY (order_product_id) REFERENCES public.tickets_orderproduct(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_accommodationinformation_limit_groups tickets_accommo_limitgroup_id_215aa00d_fk_tickets_limitgroup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_accommodationinformation_limit_groups
    ADD CONSTRAINT tickets_accommo_limitgroup_id_215aa00d_fk_tickets_limitgroup_id FOREIGN KEY (limitgroup_id) REFERENCES public.tickets_limitgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_batch tickets_batch_event_id_46c1ceb1_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_batch
    ADD CONSTRAINT tickets_batch_event_id_46c1ceb1_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_limitgroup tickets_limitgroup_event_id_aeb65dae_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_limitgroup
    ADD CONSTRAINT tickets_limitgroup_event_id_aeb65dae_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_order tickets_order_batch_id_f6bf9442_fk_tickets_batch_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order
    ADD CONSTRAINT tickets_order_batch_id_f6bf9442_fk_tickets_batch_id FOREIGN KEY (batch_id) REFERENCES public.tickets_batch(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_order tickets_order_customer_id_60494c04_fk_tickets_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order
    ADD CONSTRAINT tickets_order_customer_id_60494c04_fk_tickets_customer_id FOREIGN KEY (customer_id) REFERENCES public.tickets_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_order tickets_order_event_id_02418efc_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_order
    ADD CONSTRAINT tickets_order_event_id_02418efc_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_orderproduct tickets_orderproduct_order_id_5217f4c3_fk_tickets_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_orderproduct
    ADD CONSTRAINT tickets_orderproduct_order_id_5217f4c3_fk_tickets_order_id FOREIGN KEY (order_id) REFERENCES public.tickets_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_orderproduct tickets_orderproduct_product_id_e0ebcc8f_fk_tickets_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_orderproduct
    ADD CONSTRAINT tickets_orderproduct_product_id_e0ebcc8f_fk_tickets_product_id FOREIGN KEY (product_id) REFERENCES public.tickets_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_product tickets_product_event_id_fcae311a_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product
    ADD CONSTRAINT tickets_product_event_id_fcae311a_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_product_limit_groups tickets_product_limit_product_id_74d7bbe2_fk_tickets_product_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product_limit_groups
    ADD CONSTRAINT tickets_product_limit_product_id_74d7bbe2_fk_tickets_product_id FOREIGN KEY (product_id) REFERENCES public.tickets_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_product_limit_groups tickets_product_limitgroup_id_f1524f50_fk_tickets_limitgroup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_product_limit_groups
    ADD CONSTRAINT tickets_product_limitgroup_id_f1524f50_fk_tickets_limitgroup_id FOREIGN KEY (limitgroup_id) REFERENCES public.tickets_limitgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_shirtorder tickets_shirtorder_order_id_f1918032_fk_tickets_order_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtorder
    ADD CONSTRAINT tickets_shirtorder_order_id_f1918032_fk_tickets_order_id FOREIGN KEY (order_id) REFERENCES public.tickets_order(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_shirtorder tickets_shirtorder_size_id_15e61db1_fk_tickets_shirtsize_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtorder
    ADD CONSTRAINT tickets_shirtorder_size_id_15e61db1_fk_tickets_shirtsize_id FOREIGN KEY (size_id) REFERENCES public.tickets_shirtsize(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_shirtsize tickets_shirtsize_type_id_e6d17df8_fk_tickets_shirttype_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirtsize
    ADD CONSTRAINT tickets_shirtsize_type_id_e6d17df8_fk_tickets_shirttype_id FOREIGN KEY (type_id) REFERENCES public.tickets_shirttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_shirttype tickets_shirttype_event_id_959a8c59_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_shirttype
    ADD CONSTRAINT tickets_shirttype_event_id_959a8c59_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticketseventmeta tickets_ticketsev_pos_access_group_id_88e253da_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_ticketseventmeta
    ADD CONSTRAINT tickets_ticketsev_pos_access_group_id_88e253da_fk_auth_group_id FOREIGN KEY (pos_access_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticketseventmeta tickets_ticketseventme_admin_group_id_a37c02a1_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_ticketseventmeta
    ADD CONSTRAINT tickets_ticketseventme_admin_group_id_a37c02a1_fk_auth_group_id FOREIGN KEY (admin_group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tickets_ticketseventmeta tickets_ticketseventmeta_event_id_a24fa3fd_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tickets_ticketseventmeta
    ADD CONSTRAINT tickets_ticketseventmeta_event_id_a24fa3fd_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextra_lodging_needs traco_signupextra_id_9fe2d92a_fk_tracon11_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_lodging_needs
    ADD CONSTRAINT traco_signupextra_id_9fe2d92a_fk_tracon11_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon11_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextra_special_diet traco_signupextra_id_fc8d6f5e_fk_tracon11_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_special_diet
    ADD CONSTRAINT traco_signupextra_id_fc8d6f5e_fk_tracon11_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon11_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextra_special_diet tracon11_sig_specialdiet_id_0747ebfc_fk_tracon11_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_special_diet
    ADD CONSTRAINT tracon11_sig_specialdiet_id_0747ebfc_fk_tracon11_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.tracon11_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2_special_diet tracon11_sig_specialdiet_id_7426385d_fk_tracon11_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_special_diet
    ADD CONSTRAINT tracon11_sig_specialdiet_id_7426385d_fk_tracon11_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.tracon11_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextra_lodging_needs tracon11_signupextra_lod_night_id_30ac4159_fk_tracon11_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra_lodging_needs
    ADD CONSTRAINT tracon11_signupextra_lod_night_id_30ac4159_fk_tracon11_night_id FOREIGN KEY (night_id) REFERENCES public.tracon11_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextra tracon11_signupextra_signup_id_0aae51f1_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextra
    ADD CONSTRAINT tracon11_signupextra_signup_id_0aae51f1_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2 tracon11_signupextrav2_event_id_90e7d336_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2
    ADD CONSTRAINT tracon11_signupextrav2_event_id_90e7d336_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2_special_diet tracon11_signupextrav2_id_845e141a_fk_tracon11_signupextrav2_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_special_diet
    ADD CONSTRAINT tracon11_signupextrav2_id_845e141a_fk_tracon11_signupextrav2_id FOREIGN KEY (signupextrav2_id) REFERENCES public.tracon11_signupextrav2(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2_lodging_needs tracon11_signupextrav2_id_db124b21_fk_tracon11_signupextrav2_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_lodging_needs
    ADD CONSTRAINT tracon11_signupextrav2_id_db124b21_fk_tracon11_signupextrav2_id FOREIGN KEY (signupextrav2_id) REFERENCES public.tracon11_signupextrav2(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2_lodging_needs tracon11_signupextrav2_l_night_id_a03a048b_fk_tracon11_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2_lodging_needs
    ADD CONSTRAINT tracon11_signupextrav2_l_night_id_a03a048b_fk_tracon11_night_id FOREIGN KEY (night_id) REFERENCES public.tracon11_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon11_signupextrav2 tracon11_signupextrav2_person_id_715ff1f2_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon11_signupextrav2
    ADD CONSTRAINT tracon11_signupextrav2_person_id_715ff1f2_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_pick_your_poison tracon2017_signupext_poison_id_e429d715_fk_tracon2017_poison_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2017_signupext_poison_id_e429d715_fk_tracon2017_poison_id FOREIGN KEY (poison_id) REFERENCES public.tracon2017_poison(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra tracon2017_signupextra_event_id_e8e1ca64_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra
    ADD CONSTRAINT tracon2017_signupextra_event_id_e8e1ca64_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_pick_your_poison tracon2017_signupextra_id_50989430_fk_tracon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2017_signupextra_id_50989430_fk_tracon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_special_diet tracon2017_signupextra_id_6029da95_fk_tracon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_special_diet
    ADD CONSTRAINT tracon2017_signupextra_id_6029da95_fk_tracon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_lodging_needs tracon2017_signupextra_id_e63221b3_fk_tracon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_lodging_needs
    ADD CONSTRAINT tracon2017_signupextra_id_e63221b3_fk_tracon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_lodging_needs tracon2017_signupextra_night_id_c6ef9a96_fk_tracon2017_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_lodging_needs
    ADD CONSTRAINT tracon2017_signupextra_night_id_c6ef9a96_fk_tracon2017_night_id FOREIGN KEY (night_id) REFERENCES public.tracon2017_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra tracon2017_signupextra_person_id_c74ce6f6_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra
    ADD CONSTRAINT tracon2017_signupextra_person_id_c74ce6f6_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2017_signupextra_special_diet tracon2017_specialdiet_id_7807c41f_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2017_signupextra_special_diet
    ADD CONSTRAINT tracon2017_specialdiet_id_7807c41f_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_pick_your_poison tracon2018_signupext_poison_id_2a47a96c_fk_tracon2018_poison_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2018_signupext_poison_id_2a47a96c_fk_tracon2018_poison_id FOREIGN KEY (poison_id) REFERENCES public.tracon2018_poison(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra tracon2018_signupextra_event_id_1afcd586_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra
    ADD CONSTRAINT tracon2018_signupextra_event_id_1afcd586_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_lodging_needs tracon2018_signupextra_id_103a2d37_fk_tracon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_lodging_needs
    ADD CONSTRAINT tracon2018_signupextra_id_103a2d37_fk_tracon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_pick_your_poison tracon2018_signupextra_id_8830c7b2_fk_tracon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_pick_your_poison
    ADD CONSTRAINT tracon2018_signupextra_id_8830c7b2_fk_tracon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_special_diet tracon2018_signupextra_id_eb12e583_fk_tracon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_special_diet
    ADD CONSTRAINT tracon2018_signupextra_id_eb12e583_fk_tracon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_lodging_needs tracon2018_signupextra_night_id_1e2f6fc7_fk_tracon2018_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_lodging_needs
    ADD CONSTRAINT tracon2018_signupextra_night_id_1e2f6fc7_fk_tracon2018_night_id FOREIGN KEY (night_id) REFERENCES public.tracon2018_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra tracon2018_signupextra_person_id_907feec9_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra
    ADD CONSTRAINT tracon2018_signupextra_person_id_907feec9_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon2018_signupextra_special_diet tracon2018_specialdiet_id_8ec190aa_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon2018_signupextra_special_diet
    ADD CONSTRAINT tracon2018_specialdiet_id_8ec190aa_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon9_signupextra_special_diet tracon9_signu_specialdiet_id_bf241ca7_fk_tracon9_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_special_diet
    ADD CONSTRAINT tracon9_signu_specialdiet_id_bf241ca7_fk_tracon9_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.tracon9_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon9_signupextra_lodging_needs tracon9_signupextra_lodgi_night_id_0e266b02_fk_tracon9_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_lodging_needs
    ADD CONSTRAINT tracon9_signupextra_lodgi_night_id_0e266b02_fk_tracon9_night_id FOREIGN KEY (night_id) REFERENCES public.tracon9_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon9_signupextra tracon9_signupextra_signup_id_d4bdbbd4_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra
    ADD CONSTRAINT tracon9_signupextra_signup_id_d4bdbbd4_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon9_signupextra_lodging_needs tracon_signupextra_id_472a3533_fk_tracon9_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_lodging_needs
    ADD CONSTRAINT tracon_signupextra_id_472a3533_fk_tracon9_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon9_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tracon9_signupextra_special_diet tracon_signupextra_id_71856f9a_fk_tracon9_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracon9_signupextra_special_diet
    ADD CONSTRAINT tracon_signupextra_id_71856f9a_fk_tracon9_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.tracon9_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: traconx_signupextra_special_diet tracon_signupextra_id_8cd32bc6_fk_traconx_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_special_diet
    ADD CONSTRAINT tracon_signupextra_id_8cd32bc6_fk_traconx_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.traconx_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: traconx_signupextra_lodging_needs tracon_signupextra_id_d6ee7c08_fk_traconx_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_lodging_needs
    ADD CONSTRAINT tracon_signupextra_id_d6ee7c08_fk_traconx_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.traconx_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: traconx_signupextra_special_diet traconx_signu_specialdiet_id_8268f384_fk_traconx_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_special_diet
    ADD CONSTRAINT traconx_signu_specialdiet_id_8268f384_fk_traconx_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.traconx_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: traconx_signupextra_lodging_needs traconx_signupextra_lodgi_night_id_4f89f18a_fk_traconx_night_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra_lodging_needs
    ADD CONSTRAINT traconx_signupextra_lodgi_night_id_4f89f18a_fk_traconx_night_id FOREIGN KEY (night_id) REFERENCES public.traconx_night(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: traconx_signupextra traconx_signupextra_signup_id_e26acdca_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traconx_signupextra
    ADD CONSTRAINT traconx_signupextra_signup_id_e26acdca_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tylycon2017_signupextra tylycon2017_signupextra_event_id_d1a4bd07_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra
    ADD CONSTRAINT tylycon2017_signupextra_event_id_d1a4bd07_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tylycon2017_signupextra tylycon2017_signupextra_person_id_cde12b10_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra
    ADD CONSTRAINT tylycon2017_signupextra_person_id_cde12b10_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tylycon2017_signupextra_special_diet tylycon20_signupextra_id_cfae71a9_fk_tylycon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra_special_diet
    ADD CONSTRAINT tylycon20_signupextra_id_cfae71a9_fk_tylycon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.tylycon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tylycon2017_signupextra_special_diet tylycon20_specialdiet_id_0dbeceb6_fk_tylycon2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tylycon2017_signupextra_special_diet
    ADD CONSTRAINT tylycon20_specialdiet_id_0dbeceb6_fk_tylycon2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.tylycon2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: worldcon75_signupextra worldcon75_signupextra_event_id_6d49c550_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra
    ADD CONSTRAINT worldcon75_signupextra_event_id_6d49c550_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: worldcon75_signupextra_special_diet worldcon75_signupextra_id_3dfd4726_fk_worldcon75_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra_special_diet
    ADD CONSTRAINT worldcon75_signupextra_id_3dfd4726_fk_worldcon75_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.worldcon75_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: worldcon75_signupextra worldcon75_signupextra_person_id_36c0d651_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra
    ADD CONSTRAINT worldcon75_signupextra_person_id_36c0d651_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: worldcon75_signupextra_special_diet worldcon75_specialdiet_id_e5dfea81_fk_enrollment_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.worldcon75_signupextra_special_diet
    ADD CONSTRAINT worldcon75_specialdiet_id_e5dfea81_fk_enrollment_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.enrollment_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2016_signupextra_special_diet yu_signupextra_id_8110186d_fk_yukicon2016_signupextra_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra_special_diet
    ADD CONSTRAINT yu_signupextra_id_8110186d_fk_yukicon2016_signupextra_signup_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2016_signupextra(signup_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2016_signupextra yukicon2016_signupextra_signup_id_b360aa04_fk_labour_signup_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra
    ADD CONSTRAINT yukicon2016_signupextra_signup_id_b360aa04_fk_labour_signup_id FOREIGN KEY (signup_id) REFERENCES public.labour_signup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra_work_days yukicon2017_sig_eventday_id_42bb1342_fk_yukicon2017_eventday_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_work_days
    ADD CONSTRAINT yukicon2017_sig_eventday_id_42bb1342_fk_yukicon2017_eventday_id FOREIGN KEY (eventday_id) REFERENCES public.yukicon2017_eventday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra yukicon2017_signupextra_event_id_94e34e57_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra
    ADD CONSTRAINT yukicon2017_signupextra_event_id_94e34e57_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra yukicon2017_signupextra_person_id_73d7b8f4_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra
    ADD CONSTRAINT yukicon2017_signupextra_person_id_73d7b8f4_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra_work_days yukicon2018_sig_eventday_id_7c144f29_fk_yukicon2018_eventday_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_work_days
    ADD CONSTRAINT yukicon2018_sig_eventday_id_7c144f29_fk_yukicon2018_eventday_id FOREIGN KEY (eventday_id) REFERENCES public.yukicon2018_eventday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra yukicon2018_signupextra_event_id_4e3cc4b7_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra
    ADD CONSTRAINT yukicon2018_signupextra_event_id_4e3cc4b7_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra yukicon2018_signupextra_person_id_17b24a02_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra
    ADD CONSTRAINT yukicon2018_signupextra_person_id_17b24a02_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra_work_days yukicon2019_sig_eventday_id_15f9321c_fk_yukicon2019_eventday_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_work_days
    ADD CONSTRAINT yukicon2019_sig_eventday_id_15f9321c_fk_yukicon2019_eventday_id FOREIGN KEY (eventday_id) REFERENCES public.yukicon2019_eventday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra yukicon2019_signupextra_event_id_b03ed155_fk_core_event_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra
    ADD CONSTRAINT yukicon2019_signupextra_event_id_b03ed155_fk_core_event_id FOREIGN KEY (event_id) REFERENCES public.core_event(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra yukicon2019_signupextra_person_id_5f0a603f_fk_core_person_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra
    ADD CONSTRAINT yukicon2019_signupextra_person_id_5f0a603f_fk_core_person_id FOREIGN KEY (person_id) REFERENCES public.core_person(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra_special_diet yukicon20_signupextra_id_0644183b_fk_yukicon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_special_diet
    ADD CONSTRAINT yukicon20_signupextra_id_0644183b_fk_yukicon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra_work_days yukicon20_signupextra_id_4dd3e7bb_fk_yukicon2018_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_work_days
    ADD CONSTRAINT yukicon20_signupextra_id_4dd3e7bb_fk_yukicon2018_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2018_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra_work_days yukicon20_signupextra_id_637fae25_fk_yukicon2019_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_work_days
    ADD CONSTRAINT yukicon20_signupextra_id_637fae25_fk_yukicon2019_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2019_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra_special_diet yukicon20_signupextra_id_7df373d0_fk_yukicon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_special_diet
    ADD CONSTRAINT yukicon20_signupextra_id_7df373d0_fk_yukicon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra_special_diet yukicon20_signupextra_id_85c2763a_fk_yukicon2019_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_special_diet
    ADD CONSTRAINT yukicon20_signupextra_id_85c2763a_fk_yukicon2019_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2019_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra_work_days yukicon20_signupextra_id_e21eb43a_fk_yukicon2017_signupextra_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_work_days
    ADD CONSTRAINT yukicon20_signupextra_id_e21eb43a_fk_yukicon2017_signupextra_id FOREIGN KEY (signupextra_id) REFERENCES public.yukicon2017_signupextra(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2016_signupextra_special_diet yukicon20_specialdiet_id_249f2237_fk_yukicon2016_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2016_signupextra_special_diet
    ADD CONSTRAINT yukicon20_specialdiet_id_249f2237_fk_yukicon2016_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.yukicon2016_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2019_signupextra_special_diet yukicon20_specialdiet_id_9a6d3baa_fk_yukicon2019_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2019_signupextra_special_diet
    ADD CONSTRAINT yukicon20_specialdiet_id_9a6d3baa_fk_yukicon2019_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.yukicon2019_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2017_signupextra_special_diet yukicon20_specialdiet_id_ab802cd2_fk_yukicon2017_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2017_signupextra_special_diet
    ADD CONSTRAINT yukicon20_specialdiet_id_ab802cd2_fk_yukicon2017_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.yukicon2017_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: yukicon2018_signupextra_special_diet yukicon20_specialdiet_id_e1957e53_fk_yukicon2018_specialdiet_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yukicon2018_signupextra_special_diet
    ADD CONSTRAINT yukicon20_specialdiet_id_e1957e53_fk_yukicon2018_specialdiet_id FOREIGN KEY (specialdiet_id) REFERENCES public.yukicon2018_specialdiet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

