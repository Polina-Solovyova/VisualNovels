import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'universal-cookie';

const cookies = new Cookies();

const NovelBox = ({ imageUrl, title, description, id, isExpanded, onClick }) => {
  const [progressData, setProgressData] = useState({
    completed_episodes: 0,
    total_episodes: 0,
    progress: 0,
    status: 'New',
    current_episode: null
  });
  const navigate = useNavigate();
  const token = cookies.get('access_token');
  const props = useSpring({
    transform: isExpanded ? 'scale(1.3)' : 'scale(1)',
    config: { tension: 250, friction: 20 },
  });
  useEffect(() => {
    const fetchProgressData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/novel/${id}/progress/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        setProgressData(response.data);
      } catch (error) {
        console.error('Error fetching progress data:', error);
      }
    };

    if (id) {
      fetchProgressData();
    }
  }, [id, token]);

  const handleReadClick = () => {
    if (progressData.progress < 100) {
      navigate(`/novel/${id}/current-dialogue`);
    } else {
      console.error('Novel is already completed');
    }
  };

  const isCompleted = progressData.progress === 100;

  return (
    <div>
      <animated.div
        className={`novel-box ${isExpanded ? 'expanded' : ''}`}
        style={props}
        onClick={onClick}
      >
        <img src={imageUrl} alt={title} className="novel-image"/>
        <h3 className="novel-title">{title}</h3>
        <p className="novel-description">{description}</p>
        <div className={`novel-tag ${progressData.progress > 0 ? 'progress' : 'new'}`}>
          {progressData.progress > 0 ? `${Math.round(progressData.progress)}%` : 'New'}
        </div>
        {isExpanded && (
          <div className="expanded-content" style={{zIndex: '1000'}}>
            {progressData.total_episodes > 0 && (
                <div>
                  <h4>{progressData.status}<br/>
                    {`${progressData.completed_episodes}/${progressData.total_episodes} episodes`}</h4>
                </div>
            )}
            <button
              className="read-button"
              onClick={handleReadClick}
              disabled={isCompleted}
              style={{
                backgroundColor: isCompleted ? '#57565B' : '',
                cursor: isCompleted ? 'not-allowed' : 'pointer'
              }}
            >
              Read
            </button>
          </div>
        )}
      </animated.div>
    </div>
  );
};

export default NovelBox;
