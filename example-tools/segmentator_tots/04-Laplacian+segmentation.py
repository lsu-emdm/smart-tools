
# coding: utf-8

# # Laplacian segmentation
# 
# This notebook implements the laplacian segmentation method of [McFee and Ellis, 2014](http://bmcfee.github.io/papers/ismir2014_spectral.pdf), with a couple of minor stability improvements.

# In[28]:

from __future__ import print_function


# In[29]:

import librosa
import numpy as np
import scipy
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-muted')

# get_ipython().magic('matplotlib inline')
import sklearn.cluster


# In[36]:

#y, sr = librosa.load('audio/Karissa_Hobbs_-_09_-_Lets_Go_Fishin.mp3')
#y, sr = librosa.load('/Users/allison/Documents/_University/Teaching/_7746 MIR & ML/In Class Patches/Segmentator_tots/14 File Under Futurism.mp3',sr=44100, mono=False)
y, sr = librosa.load('media/14 File Under Futurism.mp3',sr=44100)


# In[37]:

C = librosa.logamplitude(np.abs(librosa.cqt(y=y, sr=sr,bins_per_octave=12*3, n_bins=7*12*3, real=False))**2,ref_power=np.max)


# In[38]:

plt.figure(figsize=(12, 4))
librosa.display.specshow(C, y_axis='cqt_hz', sr=sr, bins_per_octave=12*3, x_axis='time')
plt.tight_layout()

plt.draw()
plt.pause(0.001)


# In[39]:

# Let's beat-synchronize this to reduce dimensionality
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, trim=False)
Csync = librosa.util.sync(C, beats, aggregate=np.median)


# In[40]:

plt.figure(figsize=(12, 4))
librosa.display.specshow(Csync, bins_per_octave=12*3, y_axis='cqt_hz')
plt.tight_layout()


# In[41]:

# Let's build a weighted recurrence matrix from this
R = librosa.segment.recurrence_matrix(Csync, width=3, mode='affinity', sym=True)


# In[42]:

# And enhance diagonals with a median filter
df = librosa.segment.timelag_filter(scipy.ndimage.median_filter)
Rf = df(R, size=(1, 5))


# In[43]:

# Now let's build the sequence matrix using mfcc-similarity
# R_path[i, i+] = exp(-|C_i - C_j|^2 / bw)
mfcc = librosa.feature.mfcc(y=y, sr=sr)
Msync = librosa.util.sync(mfcc, beats)

path_distance = np.sum(np.diff(Msync, axis=1)**2, axis=0)
bw = np.mean(path_distance)
path_sim = np.exp(-path_distance / bw)

R_path = np.diag(path_sim, k=1) + np.diag(path_sim, k=-1)


# In[44]:

# And compute the balanced combination

deg_path = np.sum(R_path, axis=1)
deg_rec = np.sum(Rf, axis=1)

mu = deg_path.dot(deg_path + deg_rec) / np.sum((deg_path + deg_rec)**2)

A = mu * Rf + (1 - mu) * R_path


# In[45]:

plt.figure(figsize=(8, 4))
plt.subplot(1,3,1)
librosa.display.specshow(Rf, aspect='equal')
plt.title('Recurrence similarity')
plt.subplot(1,3,2)
librosa.display.specshow(R_path, aspect='equal')
plt.title('Path similarity')
plt.subplot(1,3,3)
librosa.display.specshow(A, aspect='equal')
plt.title('Combined graph')
plt.tight_layout()


# In[46]:

# Now let's compute the symmetric normalized laplacian
L = scipy.sparse.csgraph.laplacian(A, normed=True)


# In[47]:

# And its spectral decomposition
evals, evecs = scipy.linalg.eigh(L)


# In[48]:

# We can clean this up further with a median filter.
# This can help smooth over brief discontinuities
evecs = scipy.ndimage.median_filter(evecs, size=(7, 1))


# In[49]:

# cumulative normalization is needed for symmetric normalize laplacian eigenvectors
Cnorm = np.cumsum(evecs**2, axis=1)**0.5

# If we want k clusters, use the first k normalized eigenvectors.
# Fun exercise: see how segment changes as you vary k

k = 7

X = evecs[:, :k] / Cnorm[:, k-1:k]


# In[50]:

plt.figure(figsize=(8, 4))
plt.subplot(1,2,2)
librosa.display.specshow(Rf, aspect='equal')
plt.title('Recurrence matrix')

plt.subplot(1,2,1)
librosa.display.specshow(X)
plt.title('Structure components')
plt.ylabel('Time')
plt.tight_layout()


# In[51]:

# Let's use these k components to cluster
KM = sklearn.cluster.KMeans(n_clusters=k)

seg_ids = KM.fit_predict(X)


# In[52]:

plt.figure(figsize=(12, 4))
plt.subplot(1,3,2)
librosa.display.specshow(Rf, aspect='equal')
plt.title('Recurrence matrix')
plt.subplot(1,3,1)
librosa.display.specshow(X)
plt.title('Structure components')
plt.ylabel('Time')
plt.subplot(1,3,3)
librosa.display.specshow(np.atleast_2d(seg_ids).T, cmap=plt.get_cmap('Set3', k))
plt.title('Estimated segments')
plt.colorbar(ticks=range(k))
plt.tight_layout()

plt.savefig('diagrams/diagrams.png', bbox_inches='tight')

# In[53]:

# Convert the segment ids back to indices of segment boundaries
bound_beats = np.flatnonzero(seg_ids[1:] != seg_ids[:-1])


# In[54]:

# Convert beat indices to frames
bound_frames = beats[bound_beats]

# Pad this out to cover the beginning and end of the track
bound_frames = librosa.util.fix_frames(bound_frames, x_min=0, x_max=beats.max())

# And convert to time
bound_times = librosa.frames_to_time(bound_frames)


# In[57]:

bound_times
np.savetxt('/Users/allison/Documents/_University/Teaching/_7746 MIR & ML/In Class Patches/Segmentator_tots/14FUF2.txt', bound_times, fmt='%10.8f', delimiter=",") 
#np.savetxt('14FUF.txt', bound_times, fmt='%10.8f', delimiter=",") 


# In[56]:

plt.figure(figsize=(12, 4))
librosa.display.specshow(C, y_axis='cqt_hz', sr=sr, bins_per_octave=12*3, x_axis='time')
plt.vlines(bound_frames, -0.5, C.shape[0] - 0.5, color='black', linewidth=2, alpha=0.8)
plt.tight_layout()


# In[ ]:



