from faker.providers import BaseProvider


class CategoryProvider(BaseProvider):
    """
    Custom Faker provider for generating realistic assignment category names.
    """

    subjects = (
        'Illustration', 'Risk Management', 'Physiology',
        'Business Administration', 'Sports Science',
        'Performance Management', 'Genetics', 'Directing',
        'Applied Mathematics', 'Visual Arts', 'Recruitment',
        'Aerospace Engineering', 'Geography',
        'Development Economics', 'Biology',
        'Artificial Intelligence', 'Creative Writing',
        'Pharmacology', 'Surgery', 'Aesthetics', 'Microeconomics',
        'Astrophysics', 'Mobile Development', 'Music',
        'Journalism', 'Augmented Reality', 'Drawing',
        'Discrete Mathematics', 'Comparative Literature',
        'Spatial Data Analysis', 'Occupational Therapy', 'Theater',
        'Distributed Systems', 'Virtual Reality',
        'Knowledge Management', 'Speech Processing',
        'Computer Networks', 'Physiotherapy', 'Acting',
        'Mechanical Engineering', 'Sustainability', 'Robotics',
        'Political Science', 'Backend Development', 'Linguistics',
        'Sociology', 'Psychology', 'Blockchain', 'Control Systems',
        'Prose', 'Social Media Marketing', 'Metaphysics',
        'Deep Learning', 'Theology', 'Digital Marketing',
        '3D Modeling', 'Trigonometry', 'Trustworthy AI',
        'Military History', 'Bioinformatics',
        'Analytical Chemistry', 'Bioinformatics Algorithms',
        'Semantics', 'Performing Arts',
        'Object-Oriented Programming', 'Special Education',
        'Embedded Systems', 'UI Design', 'Archival Science',
        'Computer Architecture', 'Ancient History', 'Anthropology',
        'Strategic Management', 'Probabilistic Modeling',
        'Nursing', 'Ethnography', 'Dance',
        'Supply Chain Management', 'Electronics Engineering',
        'Water Resource Management', 'Systems Engineering',
        'High-Performance Computing', 'Machine Learning',
        'Environmental Science', 'Cultural History',
        'Search Engines', 'Advertising', 'Nanotechnology',
        'Microbiology', 'MLOps', 'Probability Theory',
        'Behavioral Psychology', 'Modern History', 'Singing',
        'Cloud Computing', 'Automation', 'Electrical Engineering',
        'Marketing', 'Optics', 'Graphic Design',
        'Operating Systems', 'Broadcasting', 'Economics', 'Syntax',
        'World Literature', 'Human Rights', 'Law', 'Anatomy',
        'Particle Physics', 'Logistics', 'E-Learning',
        'Climate Change', 'Change Management',
        'Operations Management', 'Music Composition',
        'Time Series Analysis', 'Auditing', 'Game Theory',
        'Environmental Policy', 'Neuroscience',
    )

    levels = (
        'Novice', 'Beginner', 'Elementary', 'Basic', 'Intermediate',
        'Upper Intermediate', 'Advanced', 'Proficient', 'Expert',
        'Specialist', 'Master',
    )

    audiences = (
        'Executives', 'Political Scientists',
        'Investment Analysts', 'Nurses', 'Recruiters',
        'Mechanical Engineers', 'Interior Designers', 'Parents',
        'Martial Artists', 'Firefighters', 'Construction Workers',
        'Marine Biologists', 'Pilates Instructors', 'Writers',
        'Cyclists', 'Biologists', 'Team Leaders',
        'Medical Doctors', 'Business Owners',
        'Supply Chain Managers', 'Police Officers', 'Auditors',
        'Authors', 'AR Developers', 'Backend Developers',
        'Startup Founders', 'Software Engineers',
        'Cybersecurity Specialists', 'Sales Managers',
        'Choreographers', 'Procurement Specialists',
        'Photographers', 'Graphic Designers', 'Paramedics',
        'Yoga Instructors', 'Database Administrators',
        'Financial Analysts', 'Linguists', 'System Administrators',
        'Robotics Engineers', 'Dancers', 'Men', 'Volunteers',
        'Jewelers', 'Cooks', 'Physicists', 'Composers',
        'Carpenters', 'Nutritionists', 'Masons',
        'Physiotherapists', 'Educators', 'Control Engineers',
        'Data Analysts', 'Entrepreneurs', 'Full-Stack Developers',
        'Seniors', 'Politicians', 'Historians',
        'Aerospace Engineers', 'Bloggers', 'Anthropologists',
        'Blockchain Developers', 'Systems Engineers',
        'Epidemiologists', 'Musicians', 'Surgeons', 'Geographers',
        'Data Scientists', 'Coaches', 'Scientists',
        'Business Analysts', 'Young Adults', 'Advisors',
        'Geologists', 'Academics', 'Psychologists', 'Pilots',
        'Architects', 'Video Editors',
    )

    patterns = (
        '{subject}',
        '{subject} ({level})',
        '{subject} for {audience}',
        '{subject} for {audience} ({level})',
    )

    def category_name(self):
        """Generate a realistic category name using simple patterns."""
        pattern = self.random_element(self.patterns)
        return pattern.format(
            subject=self.random_element(self.subjects),
            level=self.random_element(self.levels),
            audience=self.random_element(self.audiences),
        )
