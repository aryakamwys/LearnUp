document.addEventListener('DOMContentLoaded', () => {
    const courseForm = document.getElementById('courseForm');
    const coursesList = document.getElementById('coursesList');
    const submitBtn = document.getElementById('submitBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const addCourseBtn = document.getElementById('addCourseBtn');
    const overlay = document.getElementById('overlay');

    let courses = [];

    loadCourses();

    addCourseBtn.addEventListener('click', () => {
        showForm();
        resetForm();
    });

    overlay.addEventListener('click', hideForm);
    cancelBtn.addEventListener('click', hideForm);

    courseForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const courseId = document.getElementById('courseId').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const content = document.getElementById('content').value;

        try {
            if (courseId) {
                await updateCourse(courseId, { title, description, content });
                await loadCourses();
                hideForm();
            } else {
                const newCourse = await createCourse({ title, description, content });
                await loadCourses();
                hideForm();
                displayCourses(newCourse.id);
            }
        } catch (error) {
            console.error(error);
            alert("Error: " + error.message);
        }
    });

    async function graphqlRequest(query, variables = {}) {
        const res = await fetch('/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, variables })
        });
        if (!res.ok) throw new Error("Network error: " + res.status);
        const json = await res.json();
        if (json.errors) throw new Error(json.errors.map(e => e.message).join('\n'));
        if (!json.data) throw new Error("No data in GraphQL response.");
        return json.data;
    }

    async function loadCourses() {
        const query = `
            query {
                allCourses {
                    id
                    title
                    description
                    content
                }
            }
        `;
        const data = await graphqlRequest(query);
        courses = data.allCourses;
        displayCourses();
    }

    async function createCourse(input) {
        const mutation = `
            mutation($input: CreateCourseInput!) {
                createCourse(input: $input) {
                    id
                    title
                    description
                    content
                }
            }
        `;
        const data = await graphqlRequest(mutation, { input });
        return data.createCourse;
    }

    async function updateCourse(id, inputData) {
        const mutation = `
            mutation($input: UpdateCourseInput!) {
                updateCourse(input: $input) {
                    id
                }
            }
        `;
        await graphqlRequest(mutation, {
            input: { id, ...inputData }
        });
    }

    async function deleteCourse(id) {
        const mutation = `
            mutation($id: ID!) {
                deleteCourse(id: $id)
            }
        `;
        await graphqlRequest(mutation, { id });
    }

    function displayCourses(highlightId = null) {
        coursesList.innerHTML = '';
        courses.forEach(course => {
            const card = document.createElement('div');
            card.className = 'bg-white p-5 rounded-2xl shadow-md card-hover relative group';

            if (highlightId && course.id === highlightId) {
                card.classList.add('ring-2', 'ring-indigo-400');
                setTimeout(() => {
                    card.classList.remove('ring-2', 'ring-indigo-400');
                }, 2000);
            }

            card.innerHTML = `
                <div class="flex items-start justify-between mb-3">
                    <a href="/course.html?id=${course.id}" class="flex-1 hover:underline">
                        <h3 class="text-lg font-bold text-indigo-700">${course.title}</h3>
                        <p class="text-sm text-gray-600 mt-1">${course.description}</p>
                    </a>
                    <i class="fas fa-graduation-cap text-indigo-400 text-xl"></i>
                </div>
                <div class="flex justify-end gap-2 mt-4">
                    <button class="bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700" data-edit="${course.id}">
                        <i class="fas fa-edit mr-1"></i>Edit
                    </button>
                    <button class="bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700" data-delete="${course.id}">
                        <i class="fas fa-trash-alt mr-1"></i>Delete
                    </button>
                </div>
            `;

            // Tambahkan event listener tombol (jangan ikut redirect link)
            card.querySelector('[data-edit]').addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                editCourse(course.id);
            });

            card.querySelector('[data-delete]').addEventListener('click', async (e) => {
                e.stopPropagation();
                e.preventDefault();
                if (confirm("Hapus kursus ini?")) {
                    try {
                        await deleteCourse(course.id);
                        await loadCourses();
                    } catch (err) {
                        console.error(err);
                        alert("Gagal hapus: " + err.message);
                    }
                }
            });

            coursesList.appendChild(card);

            if (highlightId && course.id === highlightId) {
                setTimeout(() => {
                    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 100);
            }
        });
    }

    function editCourse(id) {
        const course = courses.find(c => c.id == id);
        if (course) {
            document.getElementById('courseId').value = course.id;
            document.getElementById('title').value = course.title;
            document.getElementById('description').value = course.description;
            document.getElementById('content').value = course.content;
            submitBtn.textContent = 'Update Course';
            showForm();
        }
    }

    function showForm() {
        courseForm.classList.remove('hidden');
        overlay.classList.remove('hidden');
    }

    function hideForm() {
        courseForm.classList.add('hidden');
        overlay.classList.add('hidden');
        resetForm();
    }

    function resetForm() {
        courseForm.reset();
        document.getElementById('courseId').value = '';
        submitBtn.textContent = 'Save';
    }
});
