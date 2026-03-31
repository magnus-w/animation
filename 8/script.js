document.addEventListener('DOMContentLoaded', () => {
    // 1. Text setup
    const poemContainer = document.getElementById('poem-container');
    const poemInner = document.createElement('div');
    poemInner.id = 'poem-inner';
    poemContainer.appendChild(poemInner);

    const poemLines = [
        "	ÅTTA MINUTER ",
        "",
        "	varje gång en solstråle träffar ditt öga",
        "		har den färdats i åtta minuter",
        "	när min tanke träffar ditt hjärta",
        "	är den tänkt i samma sekund",
        "",
        "	tankar färdas med orden,",
        "	varje nyans är en tanke",
        "		om språket dör, dör vi alla",
        "	när solen slocknar ",
        "		kan vi leva i åtta minuter"
    ];

    const lineElements = [];

    poemLines.forEach((text, i) => {
        const span = document.createElement('span');
        span.className = 'poem-line';
        span.textContent = text || ' '; // Keep space for empty lines
        poemInner.appendChild(span);
        lineElements.push(span);
    });

    // 2. Procedural Pixel Art Drawing
    function drawRetroSun() {
        const canvas = document.getElementById('sun-canvas');
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const radius = w / 2 - 2;

        ctx.clearRect(0, 0, w, h);

        // draw 16-bit dithered sun
        for (let y = 0; y < h; y++) {
            for (let x = 0; x < w; x++) {
                const dx = x - cx;
                const dy = y - cy;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist <= radius) {
                    let r = 255, g = 250, b = 210; // bright solar white/yellow
                    // Simple retro dither banding
                    if (dist > radius * 0.7) {
                        if ((x + y) % 2 === 0) {
                            r = 255; g = 200; b = 50; // yellow/orange dither
                        } else {
                            r = 255; g = 220; b = 100;
                        }
                    } else if (dist > radius * 0.85) {
                        r = 255; g = 140; b = 0; // dark orange edge
                    }

                    // pixel border
                    if (dist > radius - 1) {
                        // black edge for crisp sprite look
                        r = 30; g = 20; b = 0; 
                    }

                    ctx.fillStyle = `rgb(${r},${g},${b})`;
                    ctx.fillRect(x, y, 1, 1);
                }
            }
        }
    }

    function drawRetroEarth() {
        const canvas = document.getElementById('earth-canvas');
        const ctx = canvas.getContext('2d');
        const w = canvas.width;
        const h = canvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const radius = w / 2 - 2;

        ctx.clearRect(0, 0, w, h);

        for (let y = 0; y < h; y++) {
            for (let x = 0; x < w; x++) {
                const dx = x - cx;
                const dy = y - cy;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist <= radius) {
                    let r = 10, g = 30, b = 180; // ocean blue
                    
                    // Simple pseudo-random continents mapping
                    // Sine waves mapping spherical-ish projection
                    const nx = dx / radius;
                    const ny = dy / radius;
                    
                    // Retro shading curve
                    const shadow = (nx + ny) > 0.4 ? 0.4 : 1.0; 
                    const highlight = (nx + ny) < -0.6 ? 1.5 : 1.0;

                    // Fake continent noise
                    const noise = Math.sin(nx * 5) * Math.cos(ny * 5) + Math.sin((nx + ny) * 8);

                    if (noise > 0.3) {
                        // Land
                        r = 34; g = 139; b = 34; // standard green
                        // Dither land
                        if (noise > 0.9 && (x + y) % 2 === 0) {
                            r = 80; g = 180; b = 80;
                        }
                    } else {
                        // Dither ocean 
                        if ((x + y) % 2 === 0 && shadow === 1.0) {
                            r = 20; g = 50; b = 200;
                        }
                    }

                    // Apply shadow
                    r *= shadow * highlight;
                    g *= shadow * highlight;
                    b *= shadow * highlight;

                    // Pixel border
                    if (dist > radius - 1) {
                        r = 0; g = 10; b = 50; 
                    }

                    ctx.fillStyle = `rgb(${Math.floor(r)},${Math.floor(g)},${Math.floor(b)})`;
                    ctx.fillRect(x, y, 1, 1);
                }
            }
        }
    }

    // 3. Setup static stars
    const starsCanvas = document.getElementById('stars-canvas');
    const starsCtx = starsCanvas.getContext('2d');
    
    // Make stars canvas larger to accommodate panning
    const maxPanX = -300; // Camera moves right, so scene moves left
    const maxPanY = -800; // Camera moves down, so scene moves up
    
    starsCanvas.width = window.innerWidth - maxPanX * 2; 
    starsCanvas.height = window.innerHeight - maxPanY * 2;
    
    starsCtx.fillStyle = '#000'; // black space is already on body, but we leave transparent holes maybe? we'll just clear transparent
    starsCtx.clearRect(0,0,starsCanvas.width,starsCanvas.height);
    
    // Draw 400 random stars
    for (let i = 0; i < 400; i++) {
        const sx = Math.random() * starsCanvas.width;
        const sy = Math.random() * starsCanvas.height;
        const size = Math.random() < 0.8 ? 1 : 2; // mostly 1px, some 2px
        const brightness = Math.floor(Math.random() * 200) + 55;
        starsCtx.fillStyle = `rgb(${brightness},${brightness},${brightness})`;
        starsCtx.fillRect(sx, sy, size, size);
    }
    
    // Stardust Setup
    const sdCanvas = document.getElementById('stardust-canvas');
    const sdCtx = sdCanvas.getContext('2d');
    sdCanvas.width = window.innerWidth;
    sdCanvas.height = window.innerHeight;

    const stardustArray = [];
    for(let i = 0; i < 150; i++) {
        stardustArray.push({
            x: Math.random() * sdCanvas.width,
            y: Math.random() * sdCanvas.height,
            size: Math.random() < 0.9 ? 1 : 2,
            vx: (Math.random() - 0.5) * 0.1, // very slow drift
            vy: (Math.random() - 0.5) * 0.1,
            alpha: Math.random(),
            pulseRate: 0.005 + Math.random() * 0.01
        });
    }

    // 4. Animation logic
    drawRetroSun();
    drawRetroEarth();

    let startTime = null;
    const cameraDelayMs = 10000; // Wait 10s before camera starts panning
    const durationMs = 40000; // Faster camera movement
    const linesIntervalMs = 3500; // stagger 3.5s per line (halved)
    const firstLineDelayMs = 100; // start text almost immediately
    
    const earthLayer = document.getElementById('earth-layer');
    const sunLayer = document.getElementById('sun-layer');
    
    // Earth starts at 110vh (offscreen below) and rises to 70vh (fully visible)
    const earthStartY = window.innerHeight * 1.1;
    const earthEndY = window.innerHeight * 0.7;
    
    window.addEventListener('resize', () => {
        // Simple resize catch - just resize stardust
        sdCanvas.width = window.innerWidth;
        sdCanvas.height = window.innerHeight;
    });

    function loop(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        
        let progress = Math.min(Math.max(0, elapsed - cameraDelayMs) / durationMs, 1.0);
        
        // --- 1. Lines Dissolve ---
        lineElements.forEach((el, index) => {
            const lineTriggerTime = firstLineDelayMs + index * linesIntervalMs;
            if (elapsed >= lineTriggerTime && !el.classList.contains('visible')) {
                el.classList.add('visible');
            }
        });

        // --- 2. Parallax Pan (Stars, Sun) ---
        // Sun moves slower than stars
        const sunPxX = maxPanX * 0.1 * progress;
        const sunPxY = maxPanY * 0.1 * progress;
        sunLayer.style.transform = `translate(${sunPxX}px, ${sunPxY}px)`;
        
        const starsPxX = maxPanX * 0.2 * progress;
        const starsPxY = maxPanY * 0.2 * progress;
        starsCanvas.style.transform = `translate(${starsPxX}px, ${starsPxY}px)`;

        // --- 3. Earth Reveal ---
        const earthPxX = maxPanX * 0.3 * progress;
        const earthTranslateY = (earthEndY - earthStartY) * progress;
        earthLayer.style.transform = `translate(${earthPxX}px, ${earthTranslateY}px)`;

        // --- 4. Render Stardust ---
        sdCtx.clearRect(0,0,sdCanvas.width,sdCanvas.height);
        stardustArray.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            // wrap around
            if (p.x < 0) p.x = sdCanvas.width;
            if (p.x > sdCanvas.width) p.x = 0;
            if (p.y < 0) p.y = sdCanvas.height;
            if (p.y > sdCanvas.height) p.y = 0;
            
            p.alpha += p.pulseRate;
            if (p.alpha > 1 || p.alpha < 0) {
                p.pulseRate = -p.pulseRate; // inverse
                p.alpha = Math.max(0, Math.min(1, p.alpha));
            }
            
            sdCtx.fillStyle = `rgba(180, 200, 255, ${p.alpha})`; // slight blue twinkles
            sdCtx.fillRect(Math.floor(p.x), Math.floor(p.y), p.size, p.size);
        });

        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
});
