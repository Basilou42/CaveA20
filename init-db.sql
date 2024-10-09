-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_vins;
USE gestion_vins;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- Table des caves
CREATE TABLE IF NOT EXISTS caves (
    cave_id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table des étagères
CREATE TABLE IF NOT EXISTS etageres (
    etagere_id INT AUTO_INCREMENT PRIMARY KEY,
    num_etagere INT NOT NULL,
    emplacements INT NOT NULL,
    cave_id INT,
    FOREIGN KEY (cave_id) REFERENCES caves(cave_id) ON DELETE CASCADE
);

-- Table des bouteilles
CREATE TABLE IF NOT EXISTS bouteilles (
    bouteille_id INT AUTO_INCREMENT PRIMARY KEY,
    domaine VARCHAR(255) NOT NULL,
    nom VARCHAR(255) NOT NULL,
    type_vin VARCHAR(50),
    region VARCHAR(255),
    annee INT,
    prix DECIMAL(10, 2),
    photo VARCHAR(255),
    quantite INT DEFAULT 1,
    etagere_id INT,
    FOREIGN KEY (etagere_id) REFERENCES etageres(etagere_id) ON DELETE CASCADE
);

-- Table des notes et commentaires
CREATE TABLE IF NOT EXISTS notes_commentaires (
    id INT AUTO_INCREMENT PRIMARY KEY,
    note INT CHECK (note BETWEEN 0 AND 5),
    commentaire TEXT,
    user_id INT,
    bouteille_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (bouteille_id) REFERENCES bouteilles(bouteille_id) ON DELETE CASCADE
);

-- Création d'un index pour accélérer les recherches par cave_id et etagere_id
CREATE INDEX idx_cave ON caves(user_id);
CREATE INDEX idx_etagere ON etageres(cave_id);
CREATE INDEX idx_bouteille ON bouteilles(etagere_id);

-- Insertion d'un utilisateur par défaut
INSERT INTO users (username, password_hash) 
VALUES ('admin', SHA2('adminpassword', 256));
