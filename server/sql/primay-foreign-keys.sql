USE database_name;

ALTER TABLE Videos_CA
ADD PRIMARY KEY (video_id);

ALTER TABLE Views_CA
ADD PRIMARY KEY (video_id);

ALTER TABLE Category
ADD PRIMARY KEY (category_id, snippet_id);

ALTER TABLE Snippet
ADD PRIMARY KEY (snippet_id);

ALTER TABLE Channel_CA
ADD PRIMARY KEY (channel_id);

ALTER TABLE Location
ADD PRIMARY KEY (location_id);

-- add foreign keys

ALTER TABLE Category
ADD FOREIGN KEY (snippet_id) REFERENCES Snippet(snippet_id); 

ALTER TABLE Videos_CA
ADD FOREIGN KEY (channel_id) REFERENCES Channel_CA(channel_id),
ADD FOREIGN KEY (category_id) REFERENCES Category(category_id),
ADD FOREIGN KEY (location_id) REFERENCES Location(location_id);

ALTER TABLE Views_CA
ADD FOREIGN KEY (video_id) REFERENCES Videos_CA(video_id),
ADD FOREIGN KEY (location_id) REFERENCES Location(location_id);

ALTER TABLE Channel_CA
ADD FOREIGN KEY (location_id) REFERENCES Location(location_id);


