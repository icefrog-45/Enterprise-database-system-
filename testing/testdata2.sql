-- Data prepared by Giancarlo Pernudi Segura, pernudi@ualberta.ca, revised on 02/10/2020

drop table if exists answers;
drop table if exists questions;
drop table if exists votes;
drop table if exists tags;
drop table if exists posts;
drop table if exists ubadges;
drop table if exists badges;
drop table if exists users;
drop table if exists privileged;

create table users (
  uid		char(4),
  name		text,
  pwd     text,
  city		text,
  crdate	date,
  primary key (uid)
);
create table privileged (
  uid   char(4),
  primary key (uid),
  foreign key(uid) references users
);
create table badges (
  bname		text,
  type		text,
  primary key (bname)
);
create table ubadges (
  uid		char(4),
  bdate		date,
  bname		text,
  primary key (uid,bdate),
  foreign key (uid) references users,
  foreign key (bname) references badges
);
create table posts (
  pid		char(4),
  pdate		date,
  title		text,
  body		text,
  poster	char(4),
  primary key (pid),
  foreign key (poster) references users
);
create table tags (
  pid		char(4),
  tag		text,
  primary key (pid,tag),
  foreign key (pid) references posts
);
create table votes (
  pid		char(4),
  vno		int,
  vdate		text,
  uid		char(4),
  primary key (pid,vno),
  foreign key (pid) references posts,
  foreign key (uid) references users
);
create table questions (
  pid		char(4),
  theaid	char(4),
  primary key (pid),
  foreign key (theaid) references answers
);
create table answers (
  pid		char(4),
  qid		char(4),
  primary key (pid),
  foreign key (qid) references questions
);


insert into users values ('u001','Richard Sutton', '9sfdj32', 'Edmonton', '2018-01-05');
insert into users values ('u002','Adam White', 'dfj212dsa', 'Edmonton', '2018-06-02');
insert into users values ('u003','Alan Turing', 'sdjaf23io', 'London', '2018-02-18');
insert into users values ('u004','Linus Torvalds', 'lfs09cvxj', 'Helsinki', '2018-10-20');
insert into users values ('u005','Richard Stallman', 'j320fcjs', 'New york', '2018-12-31');
insert into users values ('u006', 'Bjarne Stroustrup', 'sfj230c', 'New York', '2019-01-01');
insert into users values ('u007', 'Ken Thompson', 'df9j31fsd', 'New Orleans', '2018-10-10');
insert into users values ('u008', 'Tom Lane', '31209fdjv', 'Madrid', '2018-11-30');
insert into users values ('u009', 'Dennis Ritchie', '390sf923', 'Bronxville', '2018-03-12');
insert into users values ('u010', 'Michael Stonebraker', '05609jfg24', 'Newburyport', '2018-09-11');

insert into badges values ('best answer', 'gold');
insert into badges values ('great question', 'gold');
insert into badges values ('exquisite answer', 'gold');
insert into badges values ('smart person', 'gold');
insert into badges values ('thought provoking question', 'gold');
insert into badges values ('intriguing question', 'silver');
insert into badges values ('gucci answer', 'silver');
insert into badges values ('bait question', 'silver');
insert into badges values ('almost correct answer', 'silver');
insert into badges values ('mediocre question', 'bronze');
insert into badges values ('mediocre answer', 'bronze');
insert into badges values ('confusing question', 'bronze');

insert into ubadges values ('u006', '2019-06-20', 'smart person');
insert into ubadges values ('u007', '2019-07-01', 'smart person');

insert into posts values ('p001', '2019-01-02', 'Exiting vim', 'How do I exit vim?', 'u001');
insert into questions values ('p001', null);
insert into tags values ('p001', 'vim');
insert into votes values ('p001', 1, '2019-01-02', 'u002');
insert into posts values ('p002', '2019-01-02', 'Easy', ':q', 'u002');
insert into answers values ('p002', 'p001');
insert into tags values('p002', 'vim');
insert into tags values('p002', 'exiting');
insert into votes values ('p002', 1, '2019-01-02', 'u003');
insert into votes values ('p002', 2, '2019-01-03', 'u004');
insert into votes values ('p002', 3, '2019-01-03', 'u005');
update questions set theaid = 'p002' where pid = 'p001';
insert into posts values ('p003', '2019-01-03', 'Turn off your computer', 'Give up and just restart your computer to exit vim.', 'u004');
insert into answers values ('p003', 'p001');
insert into tags values('p003', 'vim');
insert into tags values('p003', 'troll');
insert into tags values('p003', 'restart');
insert into ubadges values ('u001', '2019-01-03', 'great question');
insert into ubadges values ('u002', '2019-01-03', 'exquisite answer');

insert into posts values ('p004', '2019-08-07', 'SQL opinions', 'What are people''s opintions on sqlite?', 'u008');
insert into questions values('p004', null);
insert into tags values ('p004', 'relational');
insert into tags values ('p004', 'DATABASE');
insert into tags values ('p004', 'sql');
insert into tags values ('p004', 'opinion');
insert into posts values ('p005', '2019-08-12', 'My opinion', 'I like sqlite.', 'u001');
insert into answers values ('p005', 'p004');
insert into tags values ('p005', 'opinion');
insert into tags values ('p005', 'sqlite');
insert into posts values ('p006', '2019-08-13', 'My honest opinion', 'I don''t like it', 'u008');
insert into answers values ('p006', 'p004');
insert into tags values ('p006', 'opinion');
insert into ubadges values ('u008', '2019-08-09', 'great question');

insert into posts values ('p007', '2020-08-07', 'Listing hidden files/folders', 'How do I list the hidden folders and files using ls?', 'u008');
insert into questions values ('p007', null);
insert into tags values ('p007', 'ls');
insert into tags values ('p007', 'unix');
insert into tags values ('p007', 'hidden');
insert into posts values ('p008', '2020-08-15', 'Not possible', 'I don''t think that functionality exists yet.', 'u007');
insert into answers values ('p008', 'p007');
insert into tags values ('p008', 'feature');
insert into posts values ('p009', '2020-08-16', 'Figured it out', 'Turns out you just have to use the -a flag.', 'u008');
insert into answers values ('p009', 'p007');
insert into tags values ('p009', 'flag');
insert into votes values ('p009', 1, '2020-08-17', 'u005');
insert into votes values ('p009', 2, '2020-08-17', 'u009');
update questions set theaid = 'p009' where pid = 'p007';
--insert into ubadges values ('u007', '2020-08-18', 'mediorce answer');
insert into ubadges values ('u008', '2020-08-18', 'best answer');

insert into posts values ('p010', '2020-09-19', 'Lab machine ubuntu version', 'Which ubuntu version do the lab machines run?', 'u001');
insert into questions values ('p010', null);
insert into tags values ('p010', 'ubuntu');
insert into tags values ('p010', 'lab');
insert into tags values ('p010', 'version');
insert into votes values ('p010', 1, '2020-09-19', 'u002');
insert into votes values ('p010', 2, '2020-09-19', 'u004');
insert into votes values ('p010', 3, '2020-09-19', 'u006');
insert into votes values ('p010', 4, '2020-09-20', 'u008');
insert into votes values ('p010', 5, '2020-09-20', 'u010');
insert into posts values ('p011', '2020-09-20', 'Ubuntu version', 'The version is Ubuntu 16.04.7 LTS (GNU/Linux 4.15.0-112-generic x86_64).', 'u003');
insert into answers values ('p011', 'p010');
insert into tags values ('p011', 'LTS');
insert into tags values ('p011', 'version');
insert into votes values ('p011', 1, '2020-09-20', 'u001');
insert into votes values ('p011', 2, '2020-09-20', 'u002');
insert into votes values ('p011', 3, '2020-09-20', 'u006');
insert into votes values ('p011', 4, '2020-09-20', 'u007');
insert into votes values ('p011', 5, '2020-09-21', 'u009');
update questions set theaid = 'p011' where pid = 'p010';
insert into posts values ('p012', '2020-09-21', 'Lab machines version', 'The version is 16.04.', 'u004');
insert into answers values ('p012', 'p010');
insert into tags values ('p012', 'version');
insert into ubadges values ('u003', '2020-09-21', 'gucci answer');

insert into posts values ('p013', '2020-09-20', 'Relational Database', 'Does a relational database imply that there are non-relation databases?', 'u005');
insert into questions values('p013', null);
insert into tags values ('p013', 'relational');
insert into tags values ('p013', 'opposite');
insert into tags values ('p013', 'sql');
insert into posts values ('p014', '2020-09-22', 'Not sure', 'I would presume it does but I''m not completely sure.', 'u006');
insert into answers values ('p014', 'p013');
insert into votes values ('p014', 1, '2020-09-22', 'u008');
insert into posts values ('p015', '2020-09-23', 'Yes', 'There has to be', 'u009');
insert into answers values ('p015', 'p013');
insert into posts values ('p016', '2020-09-23', 'Non-SQL', 'They exist and do not use SQL. They can be more flexible than relational databases.', 'u010');
insert into answers values ('p016', 'p013');
insert into tags values ('p016', 'non-SQL');
insert into tags values ('p016', 'database');
insert into votes values ('p016', 1, '2020-09-23', 'u002');
insert into votes values ('p016', 2, '2020-09-24', 'u001');
insert into votes values ('p016', 3, '2020-09-24', 'u003');
insert into votes values ('p016', 4, '2020-09-24', 'u004');
update questions set theaid = 'p016' where pid = 'p013';
--insert into ubadges values ('u005', '2020-09-23', 'intruiging question');
insert into ubadges values ('u010', '2020-09-24', 'exquisite answer');

insert into posts values ('p017', '2020-09-20', 'Lab machines SSH', 'What is the url of the lab machines we can ssh into?', 'u004');
insert into questions values('p017', null);
insert into tags values ('p017', 'lab');
insert into tags values ('p017', 'ssh');
insert into tags values ('p017', 'url');
insert into posts values ('p018', '2020-09-21', 'ssh url', 'You can use ugXX.ca.ualberta.cs, where XX is a number.', 'u005');
insert into answers values ('p018', 'p017');
insert into votes values ('p018', 1, '2020-09-21', 'u008');
insert into posts values ('p019', '2020-09-22', 'url for ssh typo', 'The other answer has a typo. The url would instead be ugXX.cs.ualberta.ca', 'u009');
insert into answers values ('p019', 'p017');
insert into votes values ('p019', 1, '2020-09-22', 'u004');
insert into votes values ('p019', 2, '2020-09-23', 'u002');
insert into posts values ('p020', '2020-09-23', 'lab machine ssh url', 'You can simply use ohaton.cs.ualberta.ca for the ssh url.', 'u010');
insert into answers values ('p020', 'p017');
insert into tags values ('p020', 'lab');
insert into tags values ('p020', 'ssh');
insert into tags values ('p020', 'ualberta');
insert into tags values ('p020', 'url');
insert into tags values ('p020', 'cs');
insert into votes values ('p020', 1, '2020-09-23', 'u002');
insert into votes values ('p020', 2, '2020-09-24', 'u001');
insert into votes values ('p020', 3, '2020-09-24', 'u003');
insert into votes values ('p020', 4, '2020-09-24', 'u004');
update questions set theaid = 'p020' where pid = 'p017';
insert into ubadges values ('u004', '2020-09-23', 'mediocre question');
insert into ubadges values ('u005', '2020-09-24', 'exquisite answer');
insert into ubadges values ('u010', '2020-09-23', 'best answer');

insert into posts values ('p021', '2020-09-25', 'Best text editor', 'What is the best text editor?', 'u008');
insert into questions values ('p021', null);
insert into tags values ('p021', 'editor');
insert into posts values ('p022', '2020-09-25', 'vim', 'It''s minimal and comes on 99% of linux installations', 'u008');
insert into answers values ('p022', 'p021');
insert into tags values ('p022', 'editor');
insert into tags values ('p022', 'vim');
insert into posts values ('p023', '2020-09-25', 'emacs', 'It''s more powerfull.', 'u009');
insert into answers values ('p023', 'p021');
insert into tags values ('p023', 'editor');
insert into tags values ('p023', 'emacs');
