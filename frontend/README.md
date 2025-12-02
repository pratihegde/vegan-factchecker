# 🌱 Vegan Fact Checker - Frontend

A beautiful, modern React application for verifying vegan-related claims with peer-reviewed sources. Built for animal rights activists to have evidence-based responses during debates and conversations.

![Vegan Fact Checker Screenshot](screenshot.png)

## ✨ Features

- **🔍 Real-time Claim Verification** - Search peer-reviewed journals and credible sources
- **🏆 Prestigious Sources** - Results from Nature, Harvard, WHO, and top journals
- **📋 Copy-Paste Responses** - Quick talking points for debates
- **📖 Full Citations** - APA and MLA format ready to use
- **🕐 Search History** - Access past searches quickly
- **💡 Simple Explanations** - Complex science made accessible
- **❓ Common Questions** - Prepared responses to counterarguments
- **📱 Responsive Design** - Works on desktop, tablet, and mobile

## 🎨 Design

The UI follows the **activism.wtf** aesthetic with:
- Dark navy background (#0A0E27)
- Magenta accent (#FF1B8D)
- Smooth animations with Framer Motion
- Glass-morphism effects
- Professional yet activist-forward design

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- The backend API running (see backend setup)

### Installation

1. **Clone and navigate to the project:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
cp .env.example .env
```

Edit `.env` and set your API URL:
```env
VITE_API_URL=http://localhost:8000
```

4. **Start development server:**
```bash
npm run dev
```

The app will open at `http://localhost:3000`

## 📦 Building for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` folder.

## 🚢 Deployment

### GitHub Pages

1. **Update `vite.config.js`:**
```javascript
base: '/your-repo-name/'
```

2. **Build and deploy:**
```bash
npm run build
npm run deploy
```

### Vercel (Recommended)

1. Push your code to GitHub
2. Import project in Vercel
3. Add environment variable: `VITE_API_URL`
4. Deploy!

### Netlify

1. Push to GitHub
2. Connect to Netlify
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Add environment variable: `VITE_API_URL`

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool (faster than CRA)
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **React Icons** - Icon library
- **Axios** - API requests

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchBar.jsx          # Main search input
│   │   ├── VerdictCard.jsx        # Verdict display
│   │   ├── ResultsDisplay.jsx     # Results sections
│   │   ├── CollapsibleSection.jsx # Expandable sections
│   │   └── SearchHistory.jsx      # History sidebar
│   ├── utils/
│   │   ├── api.js                 # API integration
│   │   └── storage.js             # localStorage management
│   ├── App.jsx                    # Main app component
│   ├── main.jsx                   # Entry point
│   └── index.css                  # Global styles
├── public/                        # Static assets
├── index.html                     # HTML template
├── vite.config.js                 # Vite configuration
├── tailwind.config.js             # Tailwind configuration
└── package.json                   # Dependencies
```

## 🎯 Usage

### Basic Search

1. Enter a claim in the search bar
2. Click "Verify" or press Enter
3. View results with verdict, sources, and citations

### Copy Citations

- Click "Copy APA" or "Copy MLA" on any source
- Citations are copied to clipboard in proper format

### View History

- Click "Past Searches" button (top right)
- Select any previous search to reload it
- Delete individual searches or clear all

### Example Claims

Try these example claims:
- "Plants feel pain"
- "Vegans don't get enough protein"
- "B12 is only found in animal products"
- "Animal agriculture causes climate change"

## 🔧 Configuration

### API URL

Set in `.env`:
```env
VITE_API_URL=http://localhost:8000        # Local development
VITE_API_URL=https://api.example.com      # Production
```

### Demo Mode

The app includes demo data for when the API is unavailable. This allows:
- Testing the UI without a backend
- Showing to interviewers even if API is down
- Offline functionality

### Customization

**Colors** - Edit `tailwind.config.js`:
```javascript
colors: {
  magenta: {
    500: '#FF1B8D',  // Your brand color
  }
}
```

**Examples** - Edit `App.jsx`:
```javascript
const examples = ['Your', 'Custom', 'Claims']
```

## 🐛 Troubleshooting

### "API unavailable" message

- Check that backend is running
- Verify `VITE_API_URL` in `.env`
- Check browser console for errors

### Build errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Styling issues

```bash
# Rebuild Tailwind
npm run dev
```

## 📝 License

MIT License - feel free to use for your activism!

## 🤝 Contributing

Contributions welcome! This project is built to help animal rights activists.

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Design inspired by [activism.wtf](https://activism.wtf)
- Built for the vegan activist community
- Powered by peer-reviewed research

---

**Built with 💚 for animals**
