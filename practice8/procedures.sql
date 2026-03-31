CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;
CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    surnames TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1)
    LOOP
        IF phones[i] ~ '^[0-9]+$' AND length(phones[i]) >= 10 THEN

            IF EXISTS (
                SELECT 1 FROM contacts
                WHERE name = names[i] AND surname = surnames[i]
            ) THEN
                UPDATE contacts
                SET phone = phones[i]
                WHERE name = names[i] AND surname = surnames[i];
            ELSE
                INSERT INTO contacts(name, surname, phone)
                VALUES (names[i], surnames[i], phones[i]);
            END IF;

        ELSE
            RAISE NOTICE 'Invalid phone: % (% %)', phones[i], names[i], surnames[i];
        END IF;

    END LOOP;
END;
$$;
CREATE OR REPLACE PROCEDURE delete_contact(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts
    WHERE name = p_value
       OR surname = p_value
       OR phone = p_value;
END;
$$;