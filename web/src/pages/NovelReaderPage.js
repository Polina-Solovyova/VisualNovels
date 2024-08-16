import React, { useEffect, useState } from 'react';
import { getCurrentDialogue, updateProgress } from '@utils/api/apiNovels';
import { useParams, useNavigate } from 'react-router-dom';
import '../css/ReaderPage.css';


const NovelReaderPage = () => {
    const { id: novelId } = useParams();
    const [dialogue, setDialogue] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchDialogue = async () => {
            try {
                const data = await getCurrentDialogue(novelId);
                setDialogue(data);
            } catch (error) {
                console.error('Error loading dialogue:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchDialogue();
    }, [novelId]);

    const handleNextDialogue = async (e) => {
        if (e && e.target.classList.contains('choice-button')) {
            e.stopPropagation();
            return;
        }

        try {
            setLoading(true);
            const data = await updateProgress(novelId);

            if (data) {
                if (data.episode_completed) {
                    navigate('/');
                } else {
                    setDialogue(data.dialogue);
                }
            } else {
                console.warn('No dialogue data returned.');
            }
        } catch (error) {
            console.error('Error updating progress and loading next dialogue:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!dialogue) {
        return <div>No dialogue available.</div>;
    }

    return (
        <div className="reader-container" onClick={handleNextDialogue} style={{ backgroundImage: `url(${dialogue.background})` }}>
            <div className="reader-header">
                <button className="exit-button" onClick={() => window.history.back()}>Exit</button>
                <div className="progress-bar">{/* Прогресс бар */}</div>
                <button className="settings-button" onClick={() => alert('Settings not implemented yet.')}>Settings</button>
            </div>

            <div className="reader-content">
                {dialogue.character_image && (
                    <img src={dialogue.character_image} alt={dialogue.character_name} className={`character-image ${dialogue.position}`} />
                )}
                <div className={`dialogue-box ${dialogue.position}`}>
                    <p>{dialogue.text}</p>
                </div>
            </div>

            {dialogue.choices && dialogue.choices.length > 0 && (
                <div className="choices-container">
                    {dialogue.choices.map((choice) => (
                        <button
                            key={choice.id}
                            className="choice-button"
                            onClick={(e) => {
                                e.stopPropagation();
                                handleNextDialogue();
                            }}
                        >
                            {choice.text}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default NovelReaderPage;
