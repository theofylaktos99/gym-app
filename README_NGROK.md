# 🌐 Gym App με Ngrok - Οδηγίες Εγκατάστασης

## 📋 Προαπαιτούμενα

1. **Εγκατάσταση ngrok**
   - Κατεβάστε το ngrok από: https://ngrok.com/download
   - Εξάγετε το αρχείο και προσθέστε το στο PATH των Windows
   - Ή εγκαταστήστε το μέσω Chocolatey: `choco install ngrok`

2. **Δημιουργία λογαριασμού ngrok (προαιρετικό αλλά συνιστάται)**
   - Πηγαίνετε στο https://ngrok.com/signup
   - Δημιουργήστε έναν δωρεάν λογαριασμό
   - Πάρτε το auth token από το dashboard

## 🚀 Εκκίνηση της Εφαρμογής

### Μέθοδος 1: Με το Batch Script (Απλή)
```cmd
start_gym_ngrok.bat
```

### Μέθοδος 2: Με το PowerShell Script (Προτιμώμενη)
```powershell
.\start_gym_ngrok.ps1
```

### Μέθοδος 3: Χειροκίνητα

1. **Ρύθμιση Auth Token (προαιρετικό)**
   ```powershell
   # Ρύθμιση του auth token ως environment variable
   $env:NGROK_AUTH_TOKEN = "your_auth_token_here"
   ```

2. **Εγκατάσταση Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Εκκίνηση της Εφαρμογής**
   ```powershell
   python gym_app.py
   ```

## 📱 Πρόσβαση στην Εφαρμογή

Μετά την εκκίνηση, θα δείτε στο terminal:
```
🚀 Starting ngrok tunnel...
🌐 Ngrok tunnel created: https://abc123.ngrok-free.app
✅ Gym App is now accessible at: https://abc123.ngrok-free.app
✅ Share this URL to access your gym app from anywhere!
🏋️ Starting Gym App...
```

- **Τοπική Πρόσβαση**: http://localhost:5055
- **Δημόσια Πρόσβαση**: https://abc123.ngrok-free.app (το URL θα είναι διαφορετικό κάθε φορά)

## 🔐 Διαπιστευτήρια Εισόδου

- **Member ID**: 001, 002, 003, 004, 005
- **Password**: 1234 (για όλα τα Member IDs)

## � Αρχεία του Project

- `gym_app.py` - Η κύρια εφαρμογή Flask με ngrok integration
- `requirements.txt` - Python dependencies (περιλαμβάνει pyngrok)
- `start_gym_ngrok.bat` - Windows Batch script για εκκίνηση
- `start_gym_ngrok.ps1` - PowerShell script για εκκίνηση (προτιμώμενο)
- `.env.example` - Template για environment variables
- `README_NGROK.md` - Αυτό το αρχείο οδηγιών

## ✨ Χαρακτηριστικά

- **Αυτόματο ngrok tunnel**: Δημιουργείται αυτόματα όταν ξεκινάει η εφαρμογή
- **Καθαρισμός προηγούμενων sessions**: Τερματίζει τυχόν υπάρχοντα ngrok processes
- **Error handling**: Χειρίζεται σφάλματα ngrok με φιλικά μηνύματα
- **Multi-platform**: Λειτουργεί σε Windows, macOS, Linux
- **Εύκολη εκκίνηση**: Scripts για one-click εκκίνηση

## �📝 Σημειώσεις

- Το δωρεάν ngrok δίνει περιορισμένες συνδέσεις και το URL αλλάζει κάθε restart
- Για σταθερό URL, χρειάζεστε premium λογαριασμό ngrok
- Η εφαρμογή τρέχει στο port 5055
- Το ngrok tunnel δημιουργείται αυτόματα όταν ξεκινάει η εφαρμογή
- Μπορείτε να μοιραστείτε το ngrok URL με άλλους για να δοκιμάσουν την εφαρμογή

## 🛠️ Troubleshooting

### Αν δεν λειτουργεί το ngrok:
1. Βεβαιωθείτε ότι το ngrok είναι εγκατεστημένο και στο PATH
2. Ελέγξτε αν το port 5055 είναι διαθέσιμο
3. Κλείστε τυχόν άλλα ngrok processes: `taskkill /f /im ngrok.exe`
4. Δοκιμάστε χωρίς auth token αν έχετε πρόβλημα

### Αν βλέπετε "ERR_NGROK_108":
- Αυτό σημαίνει ότι έχετε ήδη ένα ngrok session ενεργό
- Η εφαρμογή θα προσπαθήσει να το τερματίσει αυτόματα
- Αν συνεχίζει το πρόβλημα, τερματίστε χειροκίνητα: `taskkill /f /im ngrok.exe`

### Αν θέλετε να σταματήσετε το ngrok:
- Απλά κλείστε την εφαρμογή (Ctrl+C)
- Το ngrok tunnel θα κλείσει αυτόματα

## 🌟 Χρήσιμες Εντολές

```powershell
# Έλεγχος αν το ngrok είναι εγκατεστημένο
ngrok version

# Ρύθμιση auth token μόνιμα
ngrok config add-authtoken your_auth_token_here

# Ανανέωση dependencies
pip install -r requirements.txt --upgrade

# Έλεγχος ενεργών ngrok processes
tasklist /fi "imagename eq ngrok.exe"

# Τερματισμός όλων των ngrok processes
taskkill /f /im ngrok.exe
```

## 🔧 Προχωρημένη Χρήση

### Χρήση με Auth Token:
1. Αντιγράψτε το `.env.example` σε `.env`
2. Προσθέστε το auth token στο `.env`
3. Το token θα φορτωθεί αυτόματα

### Χρήση με custom configuration:
Μπορείτε να τροποποιήσετε το `gym_app.py` για να αλλάξετε:
- Port number (προς το παρόν: 5055)
- Ngrok region
- Custom subdomain (με premium account)

---

**Tip**: Για καλύτερη εμπειρία, χρησιμοποιήστε το PowerShell script `start_gym_ngrok.ps1` που περιλαμβάνει έλεγχους και χρωματιστή έξοδο!