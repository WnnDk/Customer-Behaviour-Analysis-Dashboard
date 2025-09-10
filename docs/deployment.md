# Panduan Deployment

## Persiapan Deployment

### 1. File yang Diperlukan
- `requirements.txt`: Daftar dependencies
- `Procfile`: Konfigurasi untuk deployment
- `.streamlit/config.toml`: Konfigurasi Streamlit
- `.gitignore`: File yang tidak perlu di-deploy

### 2. Environment Variables
Jika menggunakan secrets atau environment variables:
1. Buat file `.streamlit/secrets.toml`
2. Tambahkan secrets yang diperlukan
3. Jangan commit file secrets ke repository

### 3. Optimasi
- Gunakan `st.cache_data` untuk data loading
- Batasi ukuran file upload (200MB)
- Implementasi error handling
- Tambahkan loading states

## Deployment ke Streamlit Cloud

1. Push code ke GitHub repository
2. Login ke [Streamlit Cloud](https://streamlit.io/cloud)
3. Pilih "New app"
4. Pilih repository dan branch
5. Set environment variables jika diperlukan
6. Deploy

## Deployment ke Heroku

1. Install Heroku CLI
2. Login ke Heroku
   ```bash
   heroku login
   ```

3. Create Heroku app
   ```bash
   heroku create your-app-name
   ```

4. Set buildpacks
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. Deploy
   ```bash
   git push heroku main
   ```

## Maintenance

### Monitoring
- Pantau penggunaan memori
- Cek error logs
- Monitor response time

### Updates
- Update dependencies secara berkala
- Test setelah update
- Backup data jika ada

### Security
- Validasi input user
- Protect endpoints
- Regular security audits

## Troubleshooting

### Common Issues
1. Memory errors
   - Kurangi ukuran data
   - Implementasi pagination
   - Optimize queries

2. Timeout errors
   - Tambahkan caching
   - Optimize heavy computations
   - Split large operations

3. Dependencies conflicts
   - Check requirements.txt
   - Use specific versions
   - Test di environment baru
