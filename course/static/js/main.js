document.addEventListener('DOMContentLoaded', () => {
    const courseForm = document.getElementById('courseForm');
    const coursesList = document.getElementById('coursesList');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');

    // Load courses when the page loads
    loadCourses();

    // Handle form submission
    courseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const courseId = document.getElementById('courseId').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const instructor = document.getElementById('instructor').value;

        const courseData = {
            title,
            description,
            instructor
        };

        try {
            if (courseId) {
                // Update existing course
                await updateCourse(courseId, courseData);
            } else {
                // Create new course
                await createCourse(courseData);
            }
            resetForm();
            loadCourses();
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while saving the course.');
        }
    });

    // Handle cancel button
    cancelBtn.addEventListener('click', () => {
        resetForm();
    });

    async function loadCourses() {
        try {
            const response = await fetch('/api/courses');
            const courses = await response.json();
            displayCourses(courses);
        } catch (error) {
            console.error('Error loading courses:', error);
            coursesList.innerHTML = '<p>Error loading courses. Please try again later.</p>';
        }
    }

    async function createCourse(courseData) {
        const response = await fetch('/api/courses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(courseData),
        });
        if (!response.ok) throw new Error('Failed to create course');
        return response.json();
    }

    async function updateCourse(id, courseData) {
        const response = await fetch(`/api/courses/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(courseData),
        });
        if (!response.ok) throw new Error('Failed to update course');
        return response.json();
    }

    async function deleteCourse(id) {
        const response = await fetch(`/api/courses/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) throw new Error('Failed to delete course');
    }

    function displayCourses(courses) {
        coursesList.innerHTML = '';
        courses.forEach(course => {
            const courseElement = document.createElement('div');
            courseElement.className = 'course-card';
            courseElement.innerHTML = `
                <h3>${course.title}</h3>
                <p><strong>Instructor:</strong> ${course.instructor}</p>
                <p>${course.description}</p>
                <div class="course-actions">
                    <button class="edit-btn" onclick="editCourse(${course.id})">Edit</button>
                    <button class="delete-btn" onclick="deleteCourseHandler(${course.id})">Delete</button>
                </div>
            `;
            coursesList.appendChild(courseElement);
        });
    }

    function editCourse(id) {
        const course = courses.find(c => c.id === id);
        if (course) {
            document.getElementById('courseId').value = course.id;
            document.getElementById('title').value = course.title;
            document.getElementById('description').value = course.description;
            document.getElementById('instructor').value = course.instructor;
            submitBtn.textContent = 'Update Course';
            cancelBtn.style.display = 'inline-block';
        }
    }

    async function deleteCourseHandler(id) {
        if (confirm('Are you sure you want to delete this course?')) {
            try {
                await deleteCourse(id);
                loadCourses();
            } catch (error) {
                console.error('Error deleting course:', error);
                alert('Failed to delete course. Please try again.');
            }
        }
    }

    function resetForm() {
        courseForm.reset();
        document.getElementById('courseId').value = '';
        submitBtn.textContent = 'Add Course';
        cancelBtn.style.display = 'none';
    }
}); 