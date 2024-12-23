'''
-- dishes

CREATE TABLE public.dishes (
    id integer NOT NULL,
    name text NOT NULL,
    description text,
    pic text,
    root text NOT NULL
);


ALTER TABLE public.dishes OWNER TO postgres;

ALTER TABLE public.dishes ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dishes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public.dishes
    ADD CONSTRAINT dishes_pkey PRIMARY KEY (id);
'''


'''
-- orders_history

CREATE TABLE public.orders_history (
    id bigint NOT NULL,
    prsn_id bigint,
    "order" text NOT NULL,
    date timestamp with time zone DEFAULT ((now() - '02:00:00'::interval))::date,
    qtys character varying(200) NOT NULL
);

ALTER TABLE public.orders_history ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.orders_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE public.orders_history OWNER TO postgres;

ALTER TABLE ONLY public.orders_history
    ADD CONSTRAINT orders_history_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.orders_history
    ADD CONSTRAINT orders_history_prsn_id_fkey FOREIGN KEY (prsn_id) REFERENCES public.users(tg_id) NOT VALID;
'''


'''
-- users

CREATE TABLE public.users (
    id bigint NOT NULL,
    tg_id bigint NOT NULL,
    name character varying(32)
);


ALTER TABLE public.users OWNER TO postgres;


ALTER TABLE public.users ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);

ALTER TABLE ONLY public.orders_history
    ADD CONSTRAINT orders_history_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.orders_history
    ADD CONSTRAINT orders_history_prsn_id_fkey FOREIGN KEY (prsn_id) REFERENCES public.users(tg_id) NOT VALID;
'''
