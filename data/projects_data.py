projects = [
    {
        "id": "project-clarix",
        "type": "project",
        "title": "Clarix – Automated Whiteboard Cleaning & Digitization System",
        "subtitle": "Raspberry Pi & Embedded Systems Project",
        "description": "Clarix is a low-cost, intelligent embedded platform designed to automate the digitization and cleaning of whiteboards. It uses computer vision, OCR, and LLMs to extract and enhance textual content, while a servo-driven brush mechanism automates erasure.",
        "data": {
            "type": "image and text data",
            "source": [
                "High-resolution images captured from whiteboards using Raspberry Pi camera module",
                "Synthetic whiteboard images created for testing OCR under different lighting and handwriting styles",
                "Annotated datasets for handwriting recognition and printed text OCR"
            ],
            "collection_method": [
                "Manual capture of live whiteboard sessions in classrooms and office environments",
                "Simulation of different board angles and lighting conditions for robustness testing",
                "Labeling of images to verify OCR accuracy"
            ],
            "preprocessing": [
                "Image enhancement: contrast adjustment, brightness normalization, and noise reduction",
                "Perspective correction to align the board surface for OCR",
                "Segmentation of text regions from diagrams and drawings",
                "Filtering out irrelevant artifacts (reflections, shadows, or smudges)"
            ],
            "volume": "Approximately 500–1000 images collected for development and testing, continuously increasing as the system is used",
            "usage": [
                "OCR model training and fine-tuning",
                "Validation of text extraction accuracy",
                "Benchmarking LLM-based text enhancement for readability and structuring"
            ]
        },
        "details": {
            "problem": "Manual whiteboard cleaning and content capture is time-consuming and error-prone, limiting productivity in classrooms and offices.",
            "solution": "Developed a Raspberry Pi-based system with a camera to capture board content, integrated OCR and LLMs for intelligent text extraction, and implemented servo-controlled brushes for automated cleaning.",
            "components": [
                "Raspberry Pi 4 as main controller",
                "Camera module for whiteboard capture",
                "Servo motors for brush movement",
                "Mechanical tracks (top & bottom) for brush mobility",
                "Brush mechanism mounted on a support frame",
                "LED indicators and buzzer for feedback",
                "Web interface for remote control and monitoring"
            ],
            "workflow": [
                "Capture high-resolution image of whiteboard",
                "Process image with OCR to extract handwritten and printed text",
                "Use LLMs to enhance extracted text and structure it logically",
                "Activate servo-driven brush mechanism to erase board content automatically",
                "Provide real-time feedback via LED and buzzer for operation status"
            ],
            "results": "Successfully automated whiteboard digitization and cleaning. Improved text capture accuracy and reduced manual cleaning time, enhancing classroom and office efficiency.",
            "challenges": [
                "Designing precise mechanical movement for consistent cleaning",
                "Integrating OCR with LLMs for structured text extraction",
                "Synchronizing hardware (servo motors, LEDs, buzzer) with software pipeline"
            ],
            "lessons_learned": [
                "Importance of mechanical and software integration for embedded projects",
                "Optimizing image capture for reliable OCR performance",
                "Creating intuitive feedback mechanisms for user interaction"
            ],
            "impact": "Enhanced productivity by automating routine whiteboard tasks, providing digital archives of content, and reducing human error. Demonstrated practical application of embedded systems combined with AI in real-world scenarios."
        },
        "technologies": ["Python", "OpenCV", "Tesseract OCR", "Flask", "LLMs", "Raspberry Pi", "Servo Motors"],
        "skills": ["Computer Vision", "Embedded Systems", "OCR", "Mechanical Design", "AI Integration", "Web Interface Development"],
        "timeframe": "May 2025 – Present",
        "organization": "Personal/Academic Project",
        "location": "Marrakesh, Morocco",
        "role": "Lead Developer",
        "supervisor": 'Mohammed Ameksa',
        "url": 'https://github.com/DarttGoblin/Clarix',
        "tags": ["Embedded Systems", "Computer Vision", "Automation", "AI", "OCR", "Python", "Raspberry Pi"],
        "context": "Clarix combines mechanical engineering, embedded systems, computer vision, OCR, and AI to automate whiteboard cleaning and digitization. The project highlights skills in both hardware and software integration and demonstrates real-world application of AI in productivity tools."
    }
]