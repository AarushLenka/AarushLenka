<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aarush Lenka | GitHub Profile</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary: #4F46E5;
            --secondary: #0EA5E9;
            --dark: #111827;
            --light: #F3F4F6;
            --accent: #10B981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, #1E293B 100%);
            color: var(--light);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        header {
            text-align: center;
            margin-bottom: 3rem;
            position: relative;
        }
        
        .gradient-text {
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-weight: 700;
            font-size: 3rem;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            color: #94A3B8;
            font-size: 1.25rem;
            margin-top: 0.5rem;
        }
        
        .glow {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(79, 70, 229, 0.3) 0%, rgba(79, 70, 229, 0) 70%);
            border-radius: 50%;
            z-index: -1;
            filter: blur(20px);
            animation: pulse 4s infinite;
        }
        
        @keyframes pulse {
            0% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
            50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.5; }
            100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
        }
        
        .card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            border-color: var(--primary);
        }
        
        .card-title {
            font-size: 1.5rem;
            color: var(--secondary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .card-content {
            color: #CBD5E1;
        }
        
        .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
        }
        
        .skill-tag {
            background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .skill-tag:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4);
        }
        
        .projects {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .project-card {
            background: rgba(17, 24, 39, 0.6);
            border-radius: 8px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        
        .project-card:hover {
            transform: translateY(-3px);
            background: rgba(17, 24, 39, 0.8);
            border-color: var(--secondary);
        }
        
        .project-title {
            font-size: 1.2rem;
            color: var(--light);
            margin-bottom: 0.5rem;
        }
        
        .project-desc {
            font-size: 0.9rem;
            color: #94A3B8;
            margin-bottom: 1rem;
        }
        
        .tech-used {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .tech-pill {
            font-size: 0.75rem;
            padding: 0.25rem 0.75rem;
            background: rgba(14, 165, 233, 0.2);
            border-radius: 12px;
            color: #7DD3FC;
        }
        
        .section-title {
            font-size: 2rem;
            margin-bottom: 1.5rem;
            color: var(--light);
            position: relative;
            display: inline-block;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            left: 0;
            bottom: -10px;
            width: 60%;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), transparent);
        }
        
        .connect {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .connect a {
            color: var(--light);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }
        
        .connect a:hover {
            color: var(--secondary);
            transform: translateY(-2px);
        }
        
        .animated-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -2;
            overflow: hidden;
        }
        
        .animated-bg::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 30% 30%, rgba(79, 70, 229, 0.2) 0%, transparent 60%),
                        radial-gradient(circle at 70% 70%, rgba(14, 165, 233, 0.2) 0%, transparent 60%);
        }
        
        .floating-circles {
            position: absolute;
            width: 100%;
            height: 100%;
        }
        
        .floating-circle {
            position: absolute;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            opacity: 0.1;
            filter: blur(8px);
            animation: float 20s infinite ease-in-out;
        }
        
        .floating-circle:nth-child(1) {
            width: 200px;
            height: 200px;
            top: 10%;
            left: 10%;
            animation-delay: 0s;
        }
        
        .floating-circle:nth-child(2) {
            width: 150px;
            height: 150px;
            top: 60%;
            left: 80%;
            animation-delay: -5s;
        }
        
        .floating-circle:nth-child(3) {
            width: 300px;
            height: 300px;
            top: 80%;
            left: 20%;
            animation-delay: -12s;
        }
        
        @keyframes float {
            0% { transform: translate(0, 0) rotate(0deg); }
            25% { transform: translate(10px, -15px) rotate(5deg); }
            50% { transform: translate(-5px, 10px) rotate(-3deg); }
            75% { transform: translate(-15px, -5px) rotate(1deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }
        
        .stats {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: rgba(17, 24, 39, 0.8);
            border-radius: 8px;
            padding: 1.5rem;
            flex: 1;
            min-width: 200px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            background: rgba(17, 24, 39, 1);
            border-color: var(--secondary);
            transform: translateY(-5px);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        .stat-label {
            font-size: 1rem;
            color: #94A3B8;
            margin-top: 0.5rem;
        }
        
        @media (max-width: 768px) {
            .gradient-text {
                font-size: 2.2rem;
            }
            
            .subtitle {
                font-size: 1rem;
            }
            
            .stats {
                flex-direction: column;
            }
            
            .projects {
                grid-template-columns: 1fr;
            }
            
            .connect {
                flex-wrap: wrap;
            }
        }
    </style>
</head>
<body>
    <div class="animated-bg">
        <div class="floating-circles">
            <div class="floating-circle"></div>
            <div class="floating-circle"></div>
            <div class="floating-circle"></div>
        </div>
    </div>
    
    <div class="container">
        <header>
            <div class="glow"></div>
            <h1 class="gradient-text">Aarush Lenka</h1>
            <p class="subtitle">Electronics and Communication Engineering Student | Tech Enthusiast</p>
        </header>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">2nd</div>
                <div class="stat-label">Year B.Tech</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">ECE</div>
                <div class="stat-label">Major</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">ISTE</div>
                <div class="stat-label">Motion Graphics Head</div>
            </div>
        </div>
        
        <section>
            <h2 class="section-title">About Me</h2>
            <div class="card">
                <div class="card-content">
                    <p>Currently pursuing my B.Tech in Electronics and Communication Engineering (2nd year). I'm passionate about building innovative projects, especially in IoT, microcontrollers, and automation. As the Motion Graphics Head at ISTE VIT, I combine my technical skills with creative design to create engaging visual content.</p>
                </div>
            </div>
        </section>
        
        <section>
            <h2 class="section-title">My Interests</h2>
            <div class="card">
                <div class="card-content">
                    <div class="skills">
                        <div class="skill-tag">Embedded Systems</div>
                        <div class="skill-tag">Microcontrollers</div>
                        <div class="skill-tag">IoT Platforms</div>
                        <div class="skill-tag">Firebase</div>
                        <div class="skill-tag">Blynk IoT</div>
                        <div class="skill-tag">Robotics</div>
                        <div class="skill-tag">Automation</div>
                        <div class="skill-tag">Motion Graphics</div>
                        <div class="skill-tag">Creative Design</div>
                        <div class="skill-tag">ESP32</div>
                        <div class="skill-tag">ESP8266</div>
                        <div class="skill-tag">Arduino</div>
                    </div>
                </div>
            </div>
        </section>
        
        <section>
            <h2 class="section-title">Featured Projects</h2>
            <div class="projects">
                <div class="project-card">
                    <h3 class="project-title">Smart Home Automation System</h3>
                    <p class="project-desc">IoT-based home automation system using ESP32 and Firebase for remote control and monitoring.</p>
                    <div class="tech-used">
                        <span class="tech-pill">ESP32</span>
                        <span class="tech-pill">Firebase</span>
                        <span class="tech-pill">IoT</span>
                    </div>
                </div>
                
                <div class="project-card">
                    <h3 class="project-title">Weather Monitoring Station</h3>
                    <p class="project-desc">Arduino-based weather station that collects and visualizes environmental data.</p>
                    <div class="tech-used">
                        <span class="tech-pill">Arduino</span>
                        <span class="tech-pill">Sensors</span>
                        <span class="tech-pill">Data Visualization</span>
                    </div>
                </div>
                
                <div class="project-card">
                    <h3 class="project-title">Motion Graphics Portfolio</h3>
                    <p class="project-desc">Creative designs and animations showcasing technical concepts through visual storytelling.</p>
                    <div class="tech-used">
                        <span class="tech-pill">After Effects</span>
                        <span class="tech-pill">Motion Design</span>
                        <span class="tech-pill">Visual Communication</span>
                    </div>
                </div>
            </div>
        </section>
        
        <section>
            <h2 class="section-title">Technical Skills</h2>
            <div class="card">
                <div class="card-title">Hardware & IoT</div>
                <div class="card-content">
                    <p>Experienced with microcontroller programming and implementation using ESP32, ESP8266, and Arduino platforms. Proficient in sensor integration, data acquisition, and building connected IoT systems.</p>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">Cloud Platforms</div>
                <div class="card-content">
                    <p>Working knowledge of Firebase and Blynk IoT for creating connected applications and services. Experienced in creating real-time data dashboards and control interfaces.</p>
                </div>
            </div>
            
            <div class="card">
                <div class="card-title">Creative Design</div>
                <div class="card-content">
                    <p>As Motion Graphics Head at ISTE VIT, I create engaging visual content that combines technical concepts with creative storytelling. Skilled in digital design tools and animation techniques.</p>
                </div>
            </div>
        </section>
        
        <div class="connect">
            <a href="https://github.com/your-username">GitHub</a>
            <a href="https://linkedin.com/in/your-username">LinkedIn</a>
            <a href="mailto:your-email@example.com">Email</a>
        </div>
    </div>
    
    <script>
        // Add subtle parallax effect to floating elements
        document.addEventListener('mousemove', (e) => {
            const circles = document.querySelectorAll('.floating-circle');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            circles.forEach((circle, index) => {
                const factor = (index + 1) * 10;
                circle.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
            });
        });
        
        // Add scroll animation for cards
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });
        
        document.querySelectorAll('.card, .project-card, .stat-card').forEach(card => {
            card.style.opacity = 0;
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease-out';
            observer.observe(card);
        });
    </script>
</body>
</html>
