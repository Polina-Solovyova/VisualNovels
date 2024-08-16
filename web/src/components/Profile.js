import React, { useState, useEffect } from 'react';
import { Button, Input, useToast } from '@chakra-ui/react';
import { API_USER } from '@utils/api/apiUser';
import NovelBox from '@components/NovelBox';

const Profile = ({ user, setUser }) => {
  const [avatar, setAvatar] = useState(null);
  const [activeTab, setActiveTab] = useState('novels');
  const [readNovels, setReadNovels] = useState([]);
  const toast = useToast();

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const profileData = await API_USER.getUserProfile();
        setUser(profileData);

        // Fetch read novels if user has progress
        if (profileData.user_progress) {
          const readNovelIds = profileData.user_progress
            .map(progress => progress.novel);
          console.log(readNovelIds)

          if (readNovelIds.length > 0) {
            const readNovelsData = await API_USER.getNovelsByIds(readNovelIds);

            // Filter out novels with tag 'new'
            const filteredNovels = readNovelsData.filter(novel => novel.tag !== 'new');
            setReadNovels(filteredNovels);
          }
        }
      } catch (error) {
        console.error('Failed to fetch user profile', error);
      }
    };

    fetchUserProfile();
  }, [setUser]);

  const getUsername = () => {
    return user.profile ? user.profile.username : 'Username not available';
  };

  const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
      setAvatar(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!avatar) {
      toast({ title: 'No file selected', status: 'warning' });
      return;
    }

    const formData = new FormData();
    formData.append('avatar', avatar);

    try {
      const response = await API_USER.uploadAvatar(formData);
      setUser((prevUser) => ({
        ...prevUser,
        profile: { ...prevUser.profile, avatar: response.avatar },
      }));
      toast({ title: 'Avatar uploaded successfully', status: 'success' });
    } catch (error) {
      console.error('Failed to upload avatar:', error);
      toast({ title: 'Failed to upload avatar', status: 'error' });
    }
  };

  return (
    <div className="profile-container">
      <div className="profile-box">
        <div className="avatar-wrapper">
          <img
            src={'http://localhost:8000/' + (user.profile.avatar || 'media/avatars/default_avatar.png')}
            alt="Avatar"
            className="avatar"
          />
        </div>
        <p className="username">{getUsername()}</p>
        <div className="navigation">
          <div className="nav-item" onClick={() => setActiveTab('novels')}>My Novels</div>
          <div className="nav-item" onClick={() => setActiveTab('achievements')}>My Achievements</div>
        </div>
        <Input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="upload-input"
        />
        <Button onClick={handleUpload} className="upload-button">Upload Avatar</Button>
      </div>
      <div className="content-box">
        {activeTab === 'novels' ? (
          user.user_progress.length > 0 ? (
            <div className="read-novels">
              <div className="tiles-container">
                {readNovels.length > 0 ? (
                  readNovels.map((novel) => (
                    <NovelBox
                      key={novel.id}
                      imageUrl={novel.cover_image}
                      title={novel.title}
                      description={novel.description}
                      id={novel.id}
                      isExpanded={false}
                      onClick={() => {}}
                    />
                  ))
                ) : (
                  <p className="no-novels">No novels</p>
                )}
              </div>
            </div>
          ) : (
            <p className="no-novels">You have not read any novels yet. <a href="/">Go to list</a></p>
          )
        ) : (
          <p className="achievements">No achievements yet!</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
