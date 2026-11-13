/* ═══════════════════════════════════════════════════════
   VOIDVEIL — Premium 3D Landing Page
   Three.js + GSAP + ScrollTrigger
   Complete JavaScript Architecture
   ═══════════════════════════════════════════════════════ */

// ─── Global State ───
const STATE = {
    mouseX: 0,
    mouseY: 0,
    normalizedMouse: { x: 0, y: 0 },
    scrollY: 0,
    isLoaded: false,
    isMobile: window.innerWidth < 768,
    scenes: {},
    animationFrameId: null
};

// ═══════════════════════════════════════════════════════
// PRELOADER
// ═══════════════════════════════════════════════════════
class Preloader {
    constructor() {
        this.el = document.getElementById('preloader');
        this.progressBar = this.el.querySelector('.preloader-progress-bar');
        this.percentEl = this.el.querySelector('.preloader-percent');
        this.progress = 0;
        this.targetProgress = 0;
    }

    start() {
        // Simulate loading progress
        const stages = [
            { target: 30, delay: 200 },
            { target: 55, delay: 600 },
            { target: 75, delay: 1000 },
            { target: 90, delay: 1500 },
            { target: 100, delay: 2200 }
        ];

        stages.forEach(({ target, delay }) => {
            setTimeout(() => {
                this.targetProgress = target;
            }, delay);
        });

        this.animate();
    }

    animate() {
        this.progress += (this.targetProgress - this.progress) * 0.08;
        this.progressBar.style.width = `${this.progress}%`;
        this.percentEl.textContent = `${Math.round(this.progress)}%`;

        if (this.progress < 99.5) {
            requestAnimationFrame(() => this.animate());
        } else {
            this.complete();
        }
    }

    complete() {
        this.progressBar.style.width = '100%';
        this.percentEl.textContent = '100%';
        
        setTimeout(() => {
            this.el.classList.add('loaded');
            STATE.isLoaded = true;
            document.body.style.overflow = 'auto';
            
            // Trigger hero animations
            heroAnimations();
        }, 400);
    }
}

// ═══════════════════════════════════════════════════════
// CUSTOM CURSOR
// ═══════════════════════════════════════════════════════
class CustomCursor {
    constructor() {
        this.dot = document.querySelector('.cursor-dot');
        this.ring = document.querySelector('.cursor-ring');
        
        if (STATE.isMobile || !this.dot) return;
        
        this.dotX = 0; this.dotY = 0;
        this.ringX = 0; this.ringY = 0;
        
        this.init();
    }

    init() {
        document.addEventListener('mousemove', (e) => {
            STATE.mouseX = e.clientX;
            STATE.mouseY = e.clientY;
            STATE.normalizedMouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            STATE.normalizedMouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
        });

        // Hover effects
        const hoverElements = document.querySelectorAll('a, button, .collection-card, .lookbook-item, .featured-image-wrap');
        hoverElements.forEach(el => {
            el.addEventListener('mouseenter', () => {
                this.dot.classList.add('hovering');
                this.ring.classList.add('hovering');
            });
            el.addEventListener('mouseleave', () => {
                this.dot.classList.remove('hovering');
                this.ring.classList.remove('hovering');
            });
        });

        this.animate();
    }

    animate() {
        // Dot follows cursor directly
        this.dotX += (STATE.mouseX - this.dotX) * 0.5;
        this.dotY += (STATE.mouseY - this.dotY) * 0.5;
        this.dot.style.left = `${this.dotX}px`;
        this.dot.style.top = `${this.dotY}px`;

        // Ring follows with lag
        this.ringX += (STATE.mouseX - this.ringX) * 0.15;
        this.ringY += (STATE.mouseY - this.ringY) * 0.15;
        this.ring.style.left = `${this.ringX}px`;
        this.ring.style.top = `${this.ringY}px`;

        requestAnimationFrame(() => this.animate());
    }
}

// ═══════════════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════════════
class Navigation {
    constructor() {
        this.navbar = document.getElementById('navbar');
        this.progressBar = this.navbar.querySelector('.nav-progress-bar');
        this.menuToggle = document.getElementById('menuToggle');
        this.mobileMenu = document.getElementById('mobileMenu');
        this.isMenuOpen = false;
        
        this.init();
    }

    init() {
        // Scroll handling
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            STATE.scrollY = scrollY;

            // Nav background
            if (scrollY > 80) {
                this.navbar.classList.add('scrolled');
            } else {
                this.navbar.classList.remove('scrolled');
            }

            // Progress bar
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const progress = (scrollY / docHeight) * 100;
            this.progressBar.style.width = `${progress}%`;
        });

        // Smooth scroll for nav links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    if (this.isMenuOpen) this.closeMenu();
                }
            });
        });

        // Mobile menu toggle
        if (this.menuToggle) {
            this.menuToggle.addEventListener('click', () => {
                this.isMenuOpen ? this.closeMenu() : this.openMenu();
            });
        }
    }

    openMenu() {
        this.isMenuOpen = true;
        this.mobileMenu.classList.add('open');
        const spans = this.menuToggle.querySelectorAll('.hamburger span');
        spans[0].style.transform = 'rotate(45deg) translate(4px, 4px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(4px, -4px)';
    }

    closeMenu() {
        this.isMenuOpen = false;
        this.mobileMenu.classList.remove('open');
        const spans = this.menuToggle.querySelectorAll('.hamburger span');
        spans[0].style.transform = '';
        spans[1].style.opacity = '';
        spans[2].style.transform = '';
    }
}

// ═══════════════════════════════════════════════════════
// THREE.JS — HERO SCENE (Planet + Stars)
// ═══════════════════════════════════════════════════════
class HeroScene {
    constructor() {
        this.canvas = document.getElementById('heroCanvas');
        if (!this.canvas) return;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas, 
            alpha: true, 
            antialias: true 
        });
        
        this.clock = new THREE.Clock();
        this.init();
    }

    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.camera.position.z = 5;

        this.createPlanet();
        this.createStars();
        this.createRings();
        this.createNebula();
        this.addLights();
        
        this.animate();
    }

    createPlanet() {
        // Main planet with custom material
        const geometry = new THREE.SphereGeometry(1.2, 64, 64);
        
        // Planet surface material
        const material = new THREE.MeshStandardMaterial({
            color: 0x1a0a3e,
            roughness: 0.7,
            metalness: 0.3,
            emissive: 0x0a0020,
            emissiveIntensity: 0.3
        });

        this.planet = new THREE.Mesh(geometry, material);
        this.planet.position.set(2.5, 0.3, 0);
        this.scene.add(this.planet);

        // Atmosphere glow
        const atmosphereGeo = new THREE.SphereGeometry(1.35, 64, 64);
        const atmosphereMat = new THREE.MeshBasicMaterial({
            color: 0xc9a0ff,
            transparent: true,
            opacity: 0.08,
            side: THREE.BackSide
        });
        this.atmosphere = new THREE.Mesh(atmosphereGeo, atmosphereMat);
        this.atmosphere.position.copy(this.planet.position);
        this.scene.add(this.atmosphere);

        // Second glow layer
        const glow2Geo = new THREE.SphereGeometry(1.5, 32, 32);
        const glow2Mat = new THREE.MeshBasicMaterial({
            color: 0x9b5de5,
            transparent: true,
            opacity: 0.03,
            side: THREE.BackSide
        });
        this.glow2 = new THREE.Mesh(glow2Geo, glow2Mat);
        this.glow2.position.copy(this.planet.position);
        this.scene.add(this.glow2);
    }

    createStars() {
        const starCount = 2000;
        const positions = new Float32Array(starCount * 3);
        const sizes = new Float32Array(starCount);
        const colors = new Float32Array(starCount * 3);

        for (let i = 0; i < starCount; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 30;
            positions[i3 + 1] = (Math.random() - 0.5) * 30;
            positions[i3 + 2] = (Math.random() - 0.5) * 30;
            
            sizes[i] = Math.random() * 2;
            
            // Color variation: white, purple, gold
            const colorChoice = Math.random();
            if (colorChoice < 0.6) {
                colors[i3] = 1; colors[i3+1] = 1; colors[i3+2] = 1;
            } else if (colorChoice < 0.85) {
                colors[i3] = 0.79; colors[i3+1] = 0.63; colors[i3+2] = 1;
            } else {
                colors[i3] = 1; colors[i3+1] = 0.84; colors[i3+2] = 0;
            }
        }

        const starGeometry = new THREE.BufferGeometry();
        starGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        starGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        starGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const starMaterial = new THREE.PointsMaterial({
            size: 0.03,
            vertexColors: true,
            transparent: true,
            opacity: 0.8,
            sizeAttenuation: true
        });

        this.stars = new THREE.Points(starGeometry, starMaterial);
        this.scene.add(this.stars);
    }

    createRings() {
        // Saturn-like ring
        const ringGeo = new THREE.RingGeometry(1.6, 2.2, 64);
        const ringMat = new THREE.MeshBasicMaterial({
            color: 0xc9a0ff,
            transparent: true,
            opacity: 0.12,
            side: THREE.DoubleSide
        });
        this.ring = new THREE.Mesh(ringGeo, ringMat);
        this.ring.position.copy(this.planet.position);
        this.ring.rotation.x = Math.PI * 0.45;
        this.ring.rotation.y = Math.PI * 0.1;
        this.scene.add(this.ring);

        // Second ring
        const ring2Geo = new THREE.RingGeometry(2.3, 2.5, 64);
        const ring2Mat = new THREE.MeshBasicMaterial({
            color: 0xffd700,
            transparent: true,
            opacity: 0.06,
            side: THREE.DoubleSide
        });
        this.ring2 = new THREE.Mesh(ring2Geo, ring2Mat);
        this.ring2.position.copy(this.planet.position);
        this.ring2.rotation.x = Math.PI * 0.45;
        this.ring2.rotation.y = Math.PI * 0.1;
        this.scene.add(this.ring2);
    }

    createNebula() {
        // Floating nebula particles
        const nebulaCount = 500;
        const positions = new Float32Array(nebulaCount * 3);
        
        for (let i = 0; i < nebulaCount; i++) {
            const i3 = i * 3;
            const radius = 2 + Math.random() * 8;
            const theta = Math.random() * Math.PI * 2;
            const phi = Math.random() * Math.PI;
            
            positions[i3] = radius * Math.sin(phi) * Math.cos(theta);
            positions[i3 + 1] = (Math.random() - 0.5) * 4;
            positions[i3 + 2] = radius * Math.sin(phi) * Math.sin(theta);
        }

        const nebulaGeo = new THREE.BufferGeometry();
        nebulaGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

        const nebulaMat = new THREE.PointsMaterial({
            size: 0.05,
            color: 0x9b5de5,
            transparent: true,
            opacity: 0.3,
            sizeAttenuation: true
        });

        this.nebula = new THREE.Points(nebulaGeo, nebulaMat);
        this.scene.add(this.nebula);
    }

    addLights() {
        // Ambient light
        const ambient = new THREE.AmbientLight(0x404080, 0.5);
        this.scene.add(ambient);

        // Point light (sun-like)
        const pointLight = new THREE.PointLight(0xc9a0ff, 1.5, 20);
        pointLight.position.set(-3, 2, 3);
        this.scene.add(pointLight);

        // Gold rim light
        const rimLight = new THREE.PointLight(0xffd700, 0.8, 15);
        rimLight.position.set(5, -1, -2);
        this.scene.add(rimLight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        const time = this.clock.getElapsedTime();
        const delta = this.clock.getDelta();

        // Rotate planet
        if (this.planet) {
            this.planet.rotation.y += 0.002;
            this.planet.position.y = 0.3 + Math.sin(time * 0.5) * 0.15;
            this.atmosphere.position.y = this.planet.position.y;
            this.glow2.position.y = this.planet.position.y;
            this.ring.position.y = this.planet.position.y;
            this.ring2.position.y = this.planet.position.y;
        }

        // Ring rotation
        if (this.ring) {
            this.ring.rotation.z += 0.001;
            this.ring2.rotation.z -= 0.0005;
        }

        // Rotate stars slowly
        if (this.stars) {
            this.stars.rotation.y += 0.0002;
            this.stars.rotation.x += 0.0001;
        }

        // Nebula rotation
        if (this.nebula) {
            this.nebula.rotation.y += 0.0003;
        }

        // Mouse-based camera movement
        this.camera.position.x += (STATE.normalizedMouse.x * 0.3 - this.camera.position.x) * 0.05;
        this.camera.position.y += (STATE.normalizedMouse.y * 0.2 - this.camera.position.y) * 0.05;
        this.camera.lookAt(this.planet ? this.planet.position : new THREE.Vector3(0, 0, 0));

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// ═══════════════════════════════════════════════════════
// THREE.JS — EXPERIENCE SCENE (Solar System)
// ═══════════════════════════════════════════════════════
class ExperienceScene {
    constructor() {
        this.canvas = document.getElementById('experienceCanvas');
        if (!this.canvas) return;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas, 
            alpha: true, 
            antialias: true 
        });
        
        this.clock = new THREE.Clock();
        this.planets = [];
        this.isVisible = false;
        this.init();
    }

    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.camera.position.set(0, 3, 10);
        this.camera.lookAt(0, 0, 0);

        this.createSun();
        this.createPlanets();
        this.createOrbitLines();
        this.createStarfield();
        this.createAsteroidBelt();
        this.addLights();
        
        // Visibility observer
        const observer = new IntersectionObserver((entries) => {
            this.isVisible = entries[0].isIntersecting;
        }, { threshold: 0.1 });
        
        const section = document.getElementById('experience');
        if (section) observer.observe(section);

        this.animate();
    }

    createSun() {
        const geo = new THREE.SphereGeometry(0.8, 32, 32);
        const mat = new THREE.MeshBasicMaterial({
            color: 0xffd700
        });
        this.sun = new THREE.Mesh(geo, mat);
        this.scene.add(this.sun);

        // Sun glow
        const glowGeo = new THREE.SphereGeometry(1.0, 32, 32);
        const glowMat = new THREE.MeshBasicMaterial({
            color: 0xffd700,
            transparent: true,
            opacity: 0.15,
            side: THREE.BackSide
        });
        const sunGlow = new THREE.Mesh(glowGeo, glowMat);
        this.scene.add(sunGlow);

        // Outer glow
        const outerGlowGeo = new THREE.SphereGeometry(1.4, 32, 32);
        const outerGlowMat = new THREE.MeshBasicMaterial({
            color: 0xffaa00,
            transparent: true,
            opacity: 0.05,
            side: THREE.BackSide
        });
        this.scene.add(new THREE.Mesh(outerGlowGeo, outerGlowMat));
    }

    createPlanets() {
        const planetData = [
            { radius: 0.15, distance: 2.0, speed: 1.8, color: 0xc9a0ff, emissive: 0x5a189a },    // Nebula Noir
            { radius: 0.2, distance: 3.0, speed: 1.2, color: 0xffd700, emissive: 0xcc8800 },       // Solar Flare
            { radius: 0.25, distance: 4.0, speed: 0.9, color: 0x00d4ff, emissive: 0x006688 },      // The Void
            { radius: 0.18, distance: 5.2, speed: 0.6, color: 0x00ff88, emissive: 0x006633 },      // Aurora Veil
            { radius: 0.35, distance: 6.8, speed: 0.4, color: 0xff6644, emissive: 0x882200 },      // Eclipse Dynasty
        ];

        planetData.forEach((data, index) => {
            // Planet body
            const geo = new THREE.SphereGeometry(data.radius, 32, 32);
            const mat = new THREE.MeshStandardMaterial({
                color: data.color,
                emissive: data.emissive,
                emissiveIntensity: 0.3,
                roughness: 0.6,
                metalness: 0.4
            });
            const planet = new THREE.Mesh(geo, mat);
            
            // Atmosphere
            const atmoGeo = new THREE.SphereGeometry(data.radius * 1.2, 32, 32);
            const atmoMat = new THREE.MeshBasicMaterial({
                color: data.color,
                transparent: true,
                opacity: 0.1,
                side: THREE.BackSide
            });
            const atmosphere = new THREE.Mesh(atmoGeo, atmoMat);
            planet.add(atmosphere);

            // Store orbit data
            planet.userData = {
                distance: data.distance,
                speed: data.speed,
                angle: (index / planetData.length) * Math.PI * 2,
                index: index
            };

            this.planets.push(planet);
            this.scene.add(planet);
        });
    }

    createOrbitLines() {
        const distances = [2.0, 3.0, 4.0, 5.2, 6.8];
        
        distances.forEach(distance => {
            const points = [];
            for (let i = 0; i <= 64; i++) {
                const angle = (i / 64) * Math.PI * 2;
                points.push(new THREE.Vector3(
                    Math.cos(angle) * distance,
                    0,
                    Math.sin(angle) * distance
                ));
            }
            
            const geo = new THREE.BufferGeometry().setFromPoints(points);
            const mat = new THREE.LineBasicMaterial({
                color: 0xc9a0ff,
                transparent: true,
                opacity: 0.08
            });
            
            this.scene.add(new THREE.Line(geo, mat));
        });
    }

    createStarfield() {
        const count = 1500;
        const positions = new Float32Array(count * 3);
        
        for (let i = 0; i < count; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 60;
            positions[i3 + 1] = (Math.random() - 0.5) * 40;
            positions[i3 + 2] = (Math.random() - 0.5) * 60;
        }

        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const mat = new THREE.PointsMaterial({
            size: 0.03,
            color: 0xffffff,
            transparent: true,
            opacity: 0.6
        });

        this.starfield = new THREE.Points(geo, mat);
        this.scene.add(this.starfield);
    }

    createAsteroidBelt() {
        const count = 300;
        const positions = new Float32Array(count * 3);
        
        for (let i = 0; i < count; i++) {
            const i3 = i * 3;
            const angle = Math.random() * Math.PI * 2;
            const distance = 5.8 + (Math.random() - 0.5) * 0.8;
            
            positions[i3] = Math.cos(angle) * distance;
            positions[i3 + 1] = (Math.random() - 0.5) * 0.3;
            positions[i3 + 2] = Math.sin(angle) * distance;
        }

        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const mat = new THREE.PointsMaterial({
            size: 0.04,
            color: 0x888888,
            transparent: true,
            opacity: 0.5
        });

        this.asteroids = new THREE.Points(geo, mat);
        this.scene.add(this.asteroids);
    }

    addLights() {
        const ambient = new THREE.AmbientLight(0x222244, 0.5);
        this.scene.add(ambient);

        const sunLight = new THREE.PointLight(0xffd700, 2, 20);
        sunLight.position.set(0, 0, 0);
        this.scene.add(sunLight);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (!this.isVisible) return;
        
        const time = this.clock.getElapsedTime();

        // Orbit planets
        this.planets.forEach(planet => {
            const d = planet.userData;
            d.angle += d.speed * 0.005;
            planet.position.x = Math.cos(d.angle) * d.distance;
            planet.position.z = Math.sin(d.angle) * d.distance;
            planet.position.y = Math.sin(d.angle * 2) * 0.2;
            planet.rotation.y += 0.01;
        });

        // Rotate asteroid belt
        if (this.asteroids) {
            this.asteroids.rotation.y += 0.0005;
        }

        // Rotate starfield
        if (this.starfield) {
            this.starfield.rotation.y += 0.0001;
        }

        // Mouse-responsive camera
        const targetX = STATE.normalizedMouse.x * 2;
        const targetY = 3 + STATE.normalizedMouse.y * 1;
        this.camera.position.x += (targetX - this.camera.position.x) * 0.02;
        this.camera.position.y += (targetY - this.camera.position.y) * 0.02;
        this.camera.lookAt(0, 0, 0);

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        if (!this.camera) return;
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// ═══════════════════════════════════════════════════════
// THREE.JS — FLOATING PARTICLES (Background)
// ═══════════════════════════════════════════════════════
class FloatingParticles {
    constructor(canvasId, sectionId) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: this.canvas, 
            alpha: true, 
            antialias: false 
        });
        
        this.isVisible = false;
        this.clock = new THREE.Clock();
        this.init(sectionId);
    }

    init(sectionId) {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
        this.camera.position.z = 5;

        // Create particles
        const count = 200;
        const positions = new Float32Array(count * 3);
        
        for (let i = 0; i < count; i++) {
            const i3 = i * 3;
            positions[i3] = (Math.random() - 0.5) * 15;
            positions[i3 + 1] = (Math.random() - 0.5) * 15;
            positions[i3 + 2] = (Math.random() - 0.5) * 10;
        }

        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        
        const mat = new THREE.PointsMaterial({
            size: 0.02,
            color: 0xc9a0ff,
            transparent: true,
            opacity: 0.4
        });

        this.particles = new THREE.Points(geo, mat);
        this.scene.add(this.particles);

        // Visibility
        const section = document.getElementById(sectionId);
        if (section) {
            const observer = new IntersectionObserver((entries) => {
                this.isVisible = entries[0].isIntersecting;
            }, { threshold: 0.1 });
            observer.observe(section);
        }

        this.animate();
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        if (!this.isVisible) return;
        
        const time = this.clock.getElapsedTime();
        
        if (this.particles) {
            this.particles.rotation.y = time * 0.05;
            this.particles.rotation.x = Math.sin(time * 0.03) * 0.1;
        }

        this.renderer.render(this.scene, this.camera);
    }

    resize() {
        if (!this.camera) return;
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }
}

// ═══════════════════════════════════════════════════════
// GSAP ANIMATIONS
// ═══════════════════════════════════════════════════════

// Register ScrollTrigger
gsap.registerPlugin(ScrollTrigger);

// ─── Hero Animations ───
function heroAnimations() {
    const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });

    tl.to('.hero-overline', {
        opacity: 1,
        y: 0,
        duration: 1,
        delay: 0.3
    })
    .to('.title-word', {
        y: 0,
        opacity: 1,
        duration: 1.2,
        stagger: 0.15,
    }, '-=0.5')
    .to('.hero-subtitle', {
        opacity: 1,
        y: 0,
        duration: 1
    }, '-=0.6')
    .to('.hero-cta-group', {
        opacity: 1,
        y: 0,
        duration: 1
    }, '-=0.6')
    .to('.hero-scroll-indicator', {
        opacity: 1,
        duration: 1
    }, '-=0.4')
    .to('.hero-side-text', {
        opacity: 0.4,
        duration: 1
    }, '-=0.8');
}

// ─── Section Header Animations ───
function initSectionAnimations() {
    // Section titles reveal
    document.querySelectorAll('.section-header').forEach(header => {
        const reveals = header.querySelectorAll('.title-reveal');
        const desc = header.querySelector('.section-desc');
        const number = header.querySelector('.section-number');

        gsap.timeline({
            scrollTrigger: {
                trigger: header,
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        })
        .from(number, { opacity: 0, y: 20, duration: 0.6 })
        .to(reveals, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            stagger: 0.12,
            ease: 'expo.out'
        }, '-=0.3')
        .to(desc, {
            opacity: 1,
            duration: 0.6,
            ease: 'power2.out'
        }, '-=0.4');
    });
}

// ─── Collection Cards Animation ───
function initCollectionAnimations() {
    gsap.utils.toArray('.collection-card').forEach((card, i) => {
        gsap.to(card, {
            opacity: 1,
            y: 0,
            rotateX: 0,
            duration: 1,
            delay: i * 0.1,
            ease: 'expo.out',
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                toggleActions: 'play none none reverse'
            }
        });

        // 3D tilt on hover
        const wrapper = card.querySelector('.card-3d-wrapper');
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            gsap.to(wrapper, {
                rotateY: x * 15,
                rotateX: -y * 10,
                duration: 0.5,
                ease: 'power2.out'
            });
        });

        card.addEventListener('mouseleave', () => {
            gsap.to(wrapper, {
                rotateY: 0,
                rotateX: 0,
                duration: 0.6,
                ease: 'elastic.out(1, 0.5)'
            });
        });
    });
}

// ─── Featured Items Animation ───
function initFeaturedAnimations() {
    gsap.utils.toArray('.featured-item').forEach((item) => {
        gsap.to(item, {
            opacity: 1,
            y: 0,
            duration: 1.2,
            ease: 'expo.out',
            scrollTrigger: {
                trigger: item,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        });

        // Parallax on featured images
        const img = item.querySelector('.featured-image');
        if (img) {
            gsap.to(img, {
                y: -30,
                ease: 'none',
                scrollTrigger: {
                    trigger: item,
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: 1
                }
            });
        }
    });
}

// ─── Story Chapters Animation ───
function initStoryAnimations() {
    gsap.utils.toArray('.story-chapter').forEach((chapter, i) => {
        const visual = chapter.querySelector('.chapter-visual');
        const text = chapter.querySelector('.chapter-text');

        const tl = gsap.timeline({
            scrollTrigger: {
                trigger: chapter,
                start: 'top 75%',
                toggleActions: 'play none none reverse'
            }
        });

        tl.to(chapter, {
            opacity: 1,
            y: 0,
            duration: 1,
            ease: 'expo.out'
        })
        .from(visual, {
            scale: 0.8,
            opacity: 0,
            duration: 0.8,
            ease: 'back.out(1.5)'
        }, '-=0.6')
        .from(text.children, {
            y: 30,
            opacity: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power2.out'
        }, '-=0.5');
    });

    // Animated counters
    gsap.utils.toArray('.stat-number').forEach(el => {
        const target = parseInt(el.getAttribute('data-target'));
        
        gsap.to(el, {
            innerText: target,
            duration: 2,
            ease: 'power2.out',
            snap: { innerText: 1 },
            scrollTrigger: {
                trigger: el,
                start: 'top 85%'
            }
        });
    });

    // Parallax background layers
    gsap.utils.toArray('.story-layer').forEach(layer => {
        const depth = parseFloat(layer.getAttribute('data-depth'));
        gsap.to(layer, {
            y: -100 * depth,
            ease: 'none',
            scrollTrigger: {
                trigger: '.story-section',
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1
            }
        });
    });
}

// ─── Lookbook Animations ───
function initLookbookAnimations() {
    gsap.utils.toArray('.lookbook-item').forEach((item, i) => {
        gsap.to(item, {
            opacity: 1,
            y: 0,
            duration: 0.8,
            delay: i * 0.08,
            ease: 'expo.out',
            scrollTrigger: {
                trigger: item,
                start: 'top 85%',
                toggleActions: 'play none none reverse'
            }
        });

        // Individual parallax
        const parallaxAmount = parseFloat(item.getAttribute('data-parallax')) || 0;
        if (parallaxAmount) {
            gsap.to(item, {
                y: parallaxAmount * 100,
                ease: 'none',
                scrollTrigger: {
                    trigger: '.lookbook-section',
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: 1
                }
            });
        }
    });
}

// ─── Marquee Velocity Effect ───
function initMarquee() {
    let velocity = 1;
    let lastScrollY = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        const diff = currentScroll - lastScrollY;
        velocity = 1 + Math.abs(diff) * 0.02;
        velocity = Math.min(velocity, 5);
        lastScrollY = currentScroll;

        const track = document.querySelector('.marquee-track');
        if (track) {
            track.style.animationDuration = `${30 / velocity}s`;
        }
    });
}

// ─── Newsletter & Footer Animations ───
function initFooterAnimations() {
    // Newsletter entrance
    gsap.from('.newsletter-content', {
        y: 60,
        opacity: 0,
        duration: 1,
        ease: 'expo.out',
        scrollTrigger: {
            trigger: '.newsletter-container',
            start: 'top 80%'
        }
    });

    // Footer grid
    gsap.from('.footer-grid > *', {
        y: 40,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
        ease: 'power2.out',
        scrollTrigger: {
            trigger: '.footer-grid',
            start: 'top 85%'
        }
    });
}

// ═══════════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    // Lock scroll during preloader
    document.body.style.overflow = 'hidden';

    // Initialize preloader
    const preloader = new Preloader();
    preloader.start();

    // Initialize cursor
    new CustomCursor();

    // Initialize navigation
    new Navigation();

    // Initialize Three.js scenes
    const heroScene = new HeroScene();
    const experienceScene = new ExperienceScene();
    const collectionsParticles = new FloatingParticles('collectionsCanvas', 'collections');
    const featuredParticles = new FloatingParticles('featuredCanvas', 'featured');

    // Initialize GSAP animations
    initSectionAnimations();
    initCollectionAnimations();
    initFeaturedAnimations();
    initStoryAnimations();
    initLookbookAnimations();
    initMarquee();
    initFooterAnimations();

    // Resize handler
    window.addEventListener('resize', () => {
        STATE.isMobile = window.innerWidth < 768;
        heroScene.resize();
        experienceScene.resize();
        if (collectionsParticles.resize) collectionsParticles.resize();
        if (featuredParticles.resize) featuredParticles.resize();
    });

    // Parallax on scroll for hero
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const hero = document.querySelector('.hero-content');
        if (hero && scrollY < window.innerHeight) {
            hero.style.transform = `translateY(${scrollY * 0.3}px)`;
            hero.style.opacity = 1 - (scrollY / window.innerHeight) * 1.5;
        }
    });
});
