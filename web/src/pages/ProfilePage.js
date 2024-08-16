import React, { useEffect, useContext, useState } from 'react';
import { UserContext } from '@providers/UserProvider';
import { API_USER } from '@utils/api/apiUser';
import Profile from '@components/Profile';
import { useToast } from '@chakra-ui/react';
import '../css/ProfilePage.css';


const ProfilePage = () => {
  const { user, setUser } = useContext(UserContext);
  const [, setReadNovels] = useState([]);
  const toast = useToast();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        // Fetch the user profile
        const data = await API_USER.getUserProfile();
        setUser({
          profile: data.profile,
          user_progress: data.user_progress
        });

        // Filter out read novels based on user progress
        if (data.user_progress) {
          // Extract IDs of novels that have been read (progress === 100)
          const readNovelIds = data.user_progress
            .map(progress => progress.novel); // Use `novel` to match your data structure
            console.log(readNovelIds)

          if (readNovelIds.length > 0) {
            // Fetch novels by IDs
            const readNovelsData = await API_USER.getNovelsByIds(readNovelIds);
            console.log(readNovelsData)
            setReadNovels(readNovelsData);
          }
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          toast({ title: 'Unauthorized. Please log in again.', status: 'error' });
        } else {
          toast({ title: 'Failed to fetch user profile', status: 'error' });
        }
      }
    };

    fetchProfile();
  }, [setUser, toast]);

  if (!user || !user.profile) {
    return <p>User not found. Please log in.</p>;
  }

  return (
    <div className="profile-page">
      <Profile user={user} setUser={setUser} />
    </div>
  );
};

export default ProfilePage;
