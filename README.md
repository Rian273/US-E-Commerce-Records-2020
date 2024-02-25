## Objectives

Project ini dibuat guna mengevaluasi konsep pembelajaran sebagai berikut:

- Mampu menggunakan Apache Airflow
- Mampu melakukan validasi data dengan menggunakan Great Expectations
- Mampu memahami konsep NoSQL secara keseluruhan.
- Mampu mempersiapkan data untuk digunakan sebelum masuk ke database NoSQL.
- Mampu mengolah dan memvisualisasikan data dengan menggunakan Kibana.

---

## Dataset

Dataset diambil dari open data repository berikut :

https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india 

---

## Project Instructions

Project dikerjakan dengan beberapa **kriteria** di bawah ini:

1. `ddl.txt`
   - File ini berisi :
      + URL dataset yang dijadikan acuan.
      + Syntax DDL untuk pembuatan database dan table.
      + Syntax DML untuk melakukan insert data ke database. Anda bisa menggunakan perintah `COPY` untuk melakukan insert data.

2. `data_raw.csv`
   - File ini berisi dataset original yang akan dimasukkan ke dalam database PostgreSQL.

3. `data_clean.csv`
   - File ini berisi data yang telah dilakukan Data Cleaning.

4. `DAG.py`
   - File yang berisi DAG untuk dijalankan dengan menggunakan Apache Airflow yang terdiri dari :
      + Python code untuk mengambil data dari database PostgreSQL.
      + Python code untuk melakukan proses Data Cleaning seperti yang sudah ditentukan dan menyimpannya ke sebuah CSV file.
      + Python code untuk me-load CSV yang berisi data yang sudah clean dan memasukkannya ke dalam Elasticsearch.

5. `conceptual.txt`.
   - File ini berisi jawaban conceptual problem.

6. `GX.ipynb`
   - File ini berisi Expectations yang digunakan untuk melakukan validasi data.

7. `/images`.
   - Folder ini berisi daftar screenshot.

---