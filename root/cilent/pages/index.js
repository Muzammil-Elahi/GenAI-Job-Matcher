import { useState } from 'react';
import Head from 'next/head';

export default function JobRecommendation() {
    const [resume, setResume] = useState(null);
    const [recommendedJobs, setRecommendedJobs] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleFileChange = (e) => {
        setResume(e.target.files[0]);
        setError(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!resume) {
            setError('Please select a resume file.');
            return;
        }
        setIsLoading(true);
        setError(null);
        const formData = new FormData();
        formData.append('resume', resume);
    
        try {
            const response = await fetch('http://127.0.0.1:8000/api/match/', {
                method: 'POST',
                body: formData,
            });
    
            if (!response.ok) {
                throw new Error('Failed to upload resume');
            }
    
            const data = await response.json();
            console.log(data);
            setRecommendedJobs(data);
        } catch (err) {
            setError('An error occurred while processing your resume. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleRefresh = () => {
        setResume(null);
        setRecommendedJobs([]);
        setError(null);
    };

    return (
        <div className="container">
            <Head>
                <title>AI Job Matcher</title>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
            </Head>

            <main>
                <h1>AI Job Matcher</h1>
                <p className="description">
                    Upload your resume and let our AI find the top 5 jobs that best match your skills and experience.
                    Our advanced algorithm analyzes your resume and compares it with thousands of job listings to
                    provide personalized job recommendations.
                </p>

                <form onSubmit={handleSubmit}>
                    <input type="file" onChange={handleFileChange} accept=".pdf,.doc,.docx" />
                    <button type="submit" disabled={isLoading}>
                        {isLoading ? 'Processing...' : 'Submit'}
                    </button>
                </form>

                {error && <p className="error">{error}</p>}

                <div className="results">
                    <h2>Recommended Jobs</h2>
                    {recommendedJobs.length > 0 ? (
                        <table>
                            <thead>
                                <tr>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Job Description</th>
                                    <th>Job Link</th>
                                </tr>
                            </thead>
                            <tbody>
                                {recommendedJobs.map((job, index) => (
                                    <tr key={index}>
                                        <td>{job._source.searched_job_title}</td>
                                        <td>{job._source.companyName}</td>
                                        <td>{job._source.location}</td>
                                        <td>{job._source.description}</td>
                                        <td>
                                        <a href={job._source.shareLink} target="_blank" rel="noopener noreferrer" className="job-link">
                                        View Job
                                            </a>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <p>No job recommendations found.</p>
                    )}
                </div>

                <button onClick={handleRefresh} className="refresh-btn">
                    Start Over
                </button>
            </main>

            <style jsx>{`
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f0f4f8;
                    color: #333;
                    font-family: Arial, sans-serif;
                }

                h1 {
                    color: #2c5282;
                    text-align: center;
                }

                .description {
                    text-align: center;
                    margin-bottom: 30px;
                    color: #4a5568;
                }

                form {
                    display: flex;
                    justify-content: center;
                    margin-bottom: 30px;
                }

                input[type="file"] {
                    margin-right: 10px;
                }

                button {
                    background-color: #4299e1;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }

                button:hover {
                    background-color: #3182ce;
                }

                button:disabled {
                    background-color: #a0aec0;
                    cursor: not-allowed;
                }

                .error {
                    color: #e53e3e;
                    text-align: center;
                }

                .results {
                    margin-top: 30px;
                }

                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }

                th, td {
                    border: 1px solid #e2e8f0;
                    padding: 12px;
                    text-align: left;
                }

                th {
                    background-color: #edf2f7;
                    font-weight: bold;
                }

                .job-link {
                    color: #4299e1;
                    text-decoration: none;
                    font-weight: bold;
                    transition: color 0.3s ease;
                }

                .job-link:hover {
                    color: #2b6cb0;
                    text-decoration: underline;
                }

                .refresh-btn {
                    display: block;
                    margin: 30px auto;
                }

                @media (max-width: 768px) {
                    table {
                        font-size: 14px;
                    }

                    th, td {
                        padding: 8px;
                    }

                    form {
                        flex-direction: column;
                        align-items: center;
                    }

                    input[type="file"] {
                        margin-right: 0;
                        margin-bottom: 10px;
                    }
                }
            `}</style>
        </div>
    );
}
