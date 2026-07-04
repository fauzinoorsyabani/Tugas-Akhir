BAB 5
KESIMPULAN DAN SARAN


5.1 Kesimpulan

Berdasarkan hasil penelitian yang telah dilakukan, dapat disimpulkan sebagai berikut:

1. Kondisi kapasitas akademik Universitas Siliwangi secara agregat masih berada di bawah batas DIKTI (1:45), dengan rata-rata rasio dosen terhadap mahasiswa per program studi pada rentang 22,8 hingga 24,9 per semester selama lima periode pelaporan (Ganjil 2023 — Ganjil 2025). Namun, terdapat disparitas struktural pada level program studi yang tersembunyi di balik nilai rata-rata tersebut: 3 program studi melampaui batas DIKTI pada periode terbaru (Pendidikan Sejarah 1:54,0; Pendidikan Masyarakat 1:50,9; Akuntansi 1:45,7), dan 4 program studi berada dalam zona waspada dengan rasio 35–45 (Ilmu Politik 1:44,0; Pendidikan Ekonomi 1:42,2; Ekonomi Pembangunan 1:39,3; Ekonomi Syari'ah 1:38,5). Analisis longitudinal menunjukkan Pendidikan Masyarakat memiliki rasio konsisten di atas batas DIKTI pada tiga dari lima periode pengamatan, mengindikasikan masalah struktural yang tidak menunjukkan perbaikan organik yang signifikan.

2. Sistem Business Intelligence yang dibangun menggunakan BI Roadmap (Moss dan Atre, 2003) berhasil mentransformasi data agregat PDDikti yang bersifat statis menjadi data warehouse terstruktur (star schema: 1 fact table + 3 dimension table, 202 rekaman) dan dashboard analitik interaktif berbasis Google Looker Studio. Sistem terbukti mendukung Decision Support System dengan menyajikan informasi kapasitas akademik secara visual, interaktif, dan tervalidasi (konsistensi data 100% antara data warehouse dan dashboard).


5.2 Keterbatasan Penelitian

Penelitian ini memiliki beberapa keterbatasan yang perlu diperhatikan dalam menginterpretasikan hasilnya:
1. Data yang digunakan merupakan data agregat yang bersumber dari portal PDDikti, sehingga analisis tidak dapat dilakukan hingga pada level individu dosen (seperti riwayat pengajaran spesifik atau NIDN/NIDK tertentu).
2. Sistem pipeline ETL saat ini belum terhubung langsung dengan basis data (API) PDDikti secara real-time, melainkan mengandalkan data hasil web scraping berkala, sehingga membutuhkan proses pembaruan data secara manual.
3. Fokus analisis masih terbatas pada rasio dosen terhadap mahasiswa sebagai indikator kuantitatif beban kerja, belum memperhitungkan kualifikasi pendidikan dosen, jabatan fungsional, dan beban tugas tambahan.

5.3 Saran

1. Memperluas cakupan analisis ke PTN BLU lain untuk benchmarking antar institusi.
2. Menambahkan variabel analisis seperti beban kerja dosen (BKD), kualifikasi akademik, dan jabatan fungsional.
3. Mengembangkan modul analisis prediktif untuk memproyeksikan kebutuhan dosen berdasarkan tren pertumbuhan mahasiswa.
4. Mengotomasi pipeline ETL agar terhubung langsung dengan sumber data (API) PDDikti secara real-time.
5. Melakukan sosialisasi dan User Acceptance Testing (UAT) kepada pemangku kepentingan institusi.
6. Menambahkan fitur notifikasi otomatis ketika rasio program studi mendekati atau melampaui batas DIKTI.
