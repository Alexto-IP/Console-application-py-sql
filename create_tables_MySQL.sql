-- Проверка на существование бд
CREATE DATABASE IF NOT EXISTS  myDB;
USE myDB;

-- Создание таблиц

CREATE TABLE supplier (
    supplier_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    supplier VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    phone_number VARCHAR(11) NOT NULL,
    country VARCHAR(50) NOT NULL
);

CREATE TABLE warehouse (
    drug_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    drug VARCHAR(30) NOT NULL,
    quantity INT(6) NOT NULL,
    price int(10) NOT NULL,
    supplier_id INT UNSIGNED NOT NULL,
    date_of_last_delivery TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES supplier (supplier_id)  ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE stufff (
    stuff_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(60) NOT NULL,
    post VARCHAR(60) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender CHAR(1) NOT NULL,
    phone_number VARCHAR(11) NOT NULL, 
    email VARCHAR(50) NOT NULL
);

CREATE TABLE buyer (
    buyer_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    buyer VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(11)
);

CREATE TABLE status (
    status_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(25) NOT NULL
);

CREATE TABLE cart(
    cart_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT UNSIGNED,
    drug_id INT UNSIGNED,
    quantity INT(6) NOT NULL,
    amount INT(9) NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (drug_id) REFERENCES warehouse (drug_id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE purchase (
    purchase_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT UNSIGNED,
    stuff_id INT UNSIGNED,
    amount int(10) NOT NULL,
    status_id INT UNSIGNED,
    date_of_purchase TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES buyer (buyer_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (stuff_id) REFERENCES stufff (stuff_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (status_id) REFERENCES status (status_id) ON DELETE CASCADE ON UPDATE RESTRICT
);