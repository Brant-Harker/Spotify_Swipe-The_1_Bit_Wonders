const fetchRecommendations = async () => {
    const response = await fetch('http://127.0.0.1:8080/api/recommendations');
    const data = await response.json();
    console.log(data);
}

fetchRecommendations();