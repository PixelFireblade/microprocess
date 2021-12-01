#!/usr/bin/perl
use CGI qw/:standard/;
use CGI::Carp qw(fatalsToBrowser);

use lib "/web/jcw/cs1917/marking/.perl/share/perl/5.10.1";
use lib "/web/jcw/cs1917/marking/.perl/lib/perl/5.10.1";

print header;

use DBI;
my $dbfile = "submissions.db";
my $dsn      = "dbi:SQLite:dbname=$dbfile";
my $user     = "";
my $password = "";
my $dbh = DBI->connect($dsn, $user, $password);

my $zid = $ENV{REMOTE_USER};

if (defined param('state')) {
my $sql = 'SELECT zid FROM half WHERE zid = ?';
my $sth = $dbh->prepare($sql);
$sth->execute($zid);
my @tempTest = $sth->fetchrow_array;
if(@tempTest) {
$dbh->do('UPDATE half SET state = ?, result = ?, time = ? WHERE zid = ?',
  undef,
  param('state'),
  param('successful'),
  param('time'),
  $zid);
} else {
$dbh->do('INSERT INTO half (zid, state, result, time) VALUES (?, ?, ?, ?)',
  undef,
  $zid, param('state'), param('successful'), param('time'));
}
}

$state = '""';
my $sql = 'SELECT state FROM half WHERE zid = ?';
my $sth = $dbh->prepare($sql);
$sth->execute($zid);
while (my @row = $sth->fetchrow_array) {
   $state = "'".$row[0]."'";
}
print <<'EOF';
<!DOCTYPE html>
<html lang="en">
	<head>
               <meta http-equiv="refresh" content="0; url=https://cgi.cse.unsw.edu.au/~cs1917ass/emulator/OLApps_SPuD/standalone/ui/half8005.html">
		<title>SPuD - Half() 8005</title>
		<script type="text/javascript" src="./lib/jquery-ui/js/jquery-1.8.0.min.js"></script>
		<script type="text/javascript" src="./lib/jquery-ui/js/jquery-ui-1.8.23.custom.min.js"></script>
		<script type="text/javascript" src="./lib/bootstrap/js/bootstrap.min.js"></script>

		<script src="./src/spud.js"></script>

		<link rel="stylesheet" type="text/css" href="./lib/bootstrap/css/bootstrap.css">

		<link type="text/css" href="./lib/jquery-ui/css/custom-theme/jquery-ui-1.8.23.custom.css" rel="stylesheet" />
		<link rel="stylesheet" type="text/css" href="./media/fonts.css">
		<link rel="stylesheet" type="text/css" href="./media/board.css">
	</head>
	<body>
			<div style="width: 970px;">
				<div id="spud"></div>
			</div>
			<center>
                        <br/>
                        When you're happy with your solution, make sure your program is in its starting state, and then click:<br/>
                        <a href="#" class="btn btn-success" id="automark-button">Check and submit my Half 8005</a>
                        <br/>
                </center>
<textarea class="hide" id="startingState">
</textarea>

<textarea class="hide" id="definition">
name: 8005
memoryBitSize: 8
numMemoryAddresses: 256
registerBitSize: 8
registerNames: IP, IS, R0, R1, SW

[descriptions]
0: Halt
1: Increment R0 (R0 = R0 + 1)
2: Decrement R0 (R0 = R0 - 1)
3: Increment R1 (R1 = R1 + 1)
4: Decrement R1 (R1 = R1 - 1)
5: Add (R0 = R0 + R1)	         				
6: Subtract (R0 = R0 - R1)
7: Print R0
8: Jump to address <data> if R0 != 0
9: Jump to address <data> if R0 == 0
10: Load <data> in to R0
11: Load <data> in to R1
12: Store R0 into address <data>
13: Store R1 into address <data>
14: Swap R0 and address <data>
15: Swap R1 and address <data>
16: Ring the bell!
17: Print R0 as an ASCII character

[instructions]
0, 1: halt.
1, 1: R0++.
2, 1: R0--.
3, 1: R1++.
4, 1: R1--.
5, 1: R0 = R0 + R1.
6, 1: R0 = R0 - R1.
7, 1: print(R0).
8, 2 case R0 != 0: IP = [IP-1].
9, 2 case R0 == 0: IP = [IP-1].
10, 2: R0 = [IP-1].
11, 2: R1 = [IP-1].
12, 2: [[IP-1]] = R0.
13, 2: [[IP-1]] = R1.
14, 2: SW = [[IP-1]]; [[IP-1]] = R0; R0 = SW.
15, 2: SW = [[IP-1]]; [[IP-1]] = R1; R1 = SW.
16, 1: bell.
17, 1: printASCII(R0).
</textarea>

<textarea class="hide" id="tests">
[
    {
        "name": "Half of 42",
        "setup": [
            {
                "type": "clearRegisters"
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 0
            },
            {
                "type": "setMemory",
                "value": 42,
                "key": 1
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 2
            },
            {
                "type": "setMemory",
                "value": 241,
                "key": 3
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 4
            },
            {
                "type": "setMemory",
                "value": 49,
                "key": 5
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 6
            },
            {
                "type": "setMemory",
                "value": 240,
                "key": 7
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 8
            },
            {
                "type": "setMemory",
                "value": 7,
                "key": 9
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 10
            },
            {
                "type": "setMemory",
                "value": 242,
                "key": 11
            },
            {
                "type": "setMemory",
                "value": 11,
                "key": 12
            },
            {
                "type": "setMemory",
                "value": 3,
                "key": 13
            },
            {
                "type": "setMemory",
                "value": 8,
                "key": 14
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 15
            },
            {
                "type": "setMemory",
                "value": 9,
                "key": 16
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 17
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 18
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 19
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 20
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 21
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 22
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 23
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 24
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 25
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 26
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 27
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 28
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 29
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 30
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 31
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 32
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 33
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 34
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 35
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 36
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 37
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 38
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 39
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 40
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 41
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 42
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 43
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 44
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 45
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 46
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 47
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 48
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 49
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 50
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 51
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 52
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 53
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 54
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 55
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 56
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 57
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 58
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 59
            }
        ],
        "test": [
            {
                "type": "register",
                "parameter": "IP",
                "match": 50,
                "correctComment": "Passed: Function returned correctly by jumping to the return address specified in the frame (49).",
                "incorrectComment": "Test Failed: Function did not return correctly by jumping to the return address specified in the frame (ie 49 in this test)"
            },
            {
                "type": "register",
                "parameter": "R0",
                "match": 21,
                "correctComment": "Passed: RO = 21. (Half of 42)",
                "incorrectComment": "Test Failed: R0 should equal 21 (Half of 42)"
            },
            {
                "type": "register",
                "parameter": "R1",
                "match": 3,
                "correctComment": "Passed: R1 was preserved",
                "incorrectComment": "Test Failed: R1 value wasn't preserved"
            }
        ]
    },
    {
        "name": "Half of 200",
        "setup": [
            {
                "type": "clearRegisters"
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 0
            },
            {
                "type": "setMemory",
                "value": 200,
                "key": 1
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 2
            },
            {
                "type": "setMemory",
                "value": 241,
                "key": 3
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 4
            },
            {
                "type": "setMemory",
                "value": 53,
                "key": 5
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 6
            },
            {
                "type": "setMemory",
                "value": 240,
                "key": 7
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 8
            },
            {
                "type": "setMemory",
                "value": 7,
                "key": 9
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 10
            },
            {
                "type": "setMemory",
                "value": 242,
                "key": 11
            },
            {
                "type": "setMemory",
                "value": 11,
                "key": 12
            },
            {
                "type": "setMemory",
                "value": 30,
                "key": 13
            },
            {
                "type": "setMemory",
                "value": 8,
                "key": 14
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 15
            },
            {
                "type": "setMemory",
                "value": 9,
                "key": 16
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 17
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 18
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 19
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 20
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 21
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 22
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 23
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 24
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 25
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 26
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 27
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 28
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 29
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 30
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 31
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 32
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 33
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 34
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 35
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 36
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 37
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 38
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 39
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 40
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 41
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 42
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 43
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 44
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 45
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 46
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 47
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 48
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 49
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 50
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 51
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 52
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 53
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 54
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 55
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 56
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 57
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 58
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 59
            }
        ],
        "test": [
            {
                "type": "register",
                "parameter": "IP",
                "match": 54,
                "correctComment": "Passed: Function returned correctly by jumping to the return address specified in the frame (53).",
                "incorrectComment": "Test Failed: Function did not return correctly by jumping to the return address specified in the frame (ie 53 in this test)"
            },
            {
                "type": "register",
                "parameter": "R0",
                "match": 100,
                "correctComment": "Passed: RO = 100. (Half of 200)",
                "incorrectComment": "Test Failed: R0 should equal 100. (Half of 200)"
            },
            {
                "type": "register",
                "parameter": "R1",
                "match": 30,
                "correctComment": "Passed: R1 was preserved",
                "incorrectComment": "Test Failed: R1 value wasn't preserved"
            }
        ]
    },
    {
        "name": "Half of 0",
        "setup": [
            {
                "type": "clearRegisters"
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 0
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 1
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 2
            },
            {
                "type": "setMemory",
                "value": 241,
                "key": 3
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 4
            },
            {
                "type": "setMemory",
                "value": 48,
                "key": 5
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 6
            },
            {
                "type": "setMemory",
                "value": 240,
                "key": 7
            },
            {
                "type": "setMemory",
                "value": 10,
                "key": 8
            },
            {
                "type": "setMemory",
                "value": 7,
                "key": 9
            },
            {
                "type": "setMemory",
                "value": 12,
                "key": 10
            },
            {
                "type": "setMemory",
                "value": 242,
                "key": 11
            },
            {
                "type": "setMemory",
                "value": 11,
                "key": 12
            },
            {
                "type": "setMemory",
                "value": 33,
                "key": 13
            },
            {
                "type": "setMemory",
                "value": 8,
                "key": 14
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 15
            },
            {
                "type": "setMemory",
                "value": 9,
                "key": 16
            },
            {
                "type": "setMemory",
                "value": 60,
                "key": 17
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 18
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 19
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 20
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 21
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 22
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 23
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 24
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 25
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 26
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 27
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 28
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 29
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 30
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 31
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 32
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 33
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 34
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 35
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 36
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 37
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 38
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 39
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 40
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 41
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 42
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 43
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 44
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 45
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 46
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 47
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 48
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 49
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 50
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 51
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 52
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 53
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 54
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 55
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 56
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 57
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 58
            },
            {
                "type": "setMemory",
                "value": 0,
                "key": 59
            }
        ],
        "test": [
            {
                "type": "register",
                "parameter": "IP",
                "match": 49,
                "correctComment": "Passed: Function returned correctly by jumping to the return address specified in the frame (48).",
                "incorrectComment": "Test Failed: Function did not return correctly by jumping to the return address specified in the frame (ie 48 in this test)"
            },
            {
                "type": "register",
                "parameter": "R0",
                "match": 0,
                "correctComment": "Passed: RO = 0. (Half of 0)",
                "incorrectComment": "Test Failed: R0 should equal 0. (Half of 0)"
            },
            {
                "type": "register",
                "parameter": "R1",
                "match": 33,
                "correctComment": "Passed: R1 was preserved",
                "incorrectComment": "Test Failed: R1 value wasn't preserved"
            }
        ]
    }
]

</textarea>
<form id="progress" style="display:none;" class="hide" action="#" method="post">
<textarea form="progress" name="state" id="state" style="display:none;" class="hide"></textarea>
<textarea form="progress" name="successful" id="successful" style="display:none;" class="hide"></textarea>
<textarea form="progress" name="time" id="time" style="display:none;" class="hide"></textarea>
</form>
		<script>
EOF
print "var state = $state;";
print <<'EOF';
	        </script>
                <script src="data:text/javascript;base64,dmFyIHRlc3RzO3RyeXt0ZXN0cz1KU09OLnBhcnNlKCQoIiN0ZXN0cyIpLnRleHQoKSl9Y2F0Y2goZXJyKXtjb25zb2xlLmxvZygkKCIjdGVzdHMiKS50ZXh0KCkpLGFsZXJ0KGVycil9dmFyIHNhdmVGdW5jPWZ1bmN0aW9uKHQpe3N0YXRlPUpTT04uc3RyaW5naWZ5KHQpLGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzdGF0ZSIpLmlubmVySFRNTD1zdGF0ZTt2YXIgZT1uZXcgRGF0ZTtkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgidGltZSIpLmlubmVySFRNTD1lLnRvSVNPU3RyaW5nKCksZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInByb2dyZXNzIikuc3VibWl0KCl9LGxvYWRGdW5jPWZ1bmN0aW9uKHQpe3QoSlNPTi5wYXJzZShzdGF0ZSkpfSxsb2FkQXBwPWZ1bmN0aW9uKHQsZSxuKXskKCIjc3B1ZCIpLnNwdWQoe2RlZmluaXRpb246JCgiI2RlZmluaXRpb24iKS50ZXh0KCksc3RhcnRpbmdTdGF0ZTokKCIjc3RhcnRpbmdTdGF0ZSIpLnRleHQoKSx3b3JrZXJTY3JpcHQ6Ii4vc3JjL3NwdWRFbXUuanMiLGF1ZGlvOnQsb25TYXZlOmUsb25Mb2FkOm59KX07bG9hZEFwcCh2b2lkIDAsc2F2ZUZ1bmMsbG9hZEZ1bmMpO3ZhciBzYXZlTWFya3M9ZnVuY3Rpb24odCl7Y29uc29sZS5sb2coIk1BUktTOiIpLGNvbnNvbGUubG9nKHQpO2Zvcih2YXIgZT0iIixuPXQubGVuZ3RoLHM9MDtuPnM7cysrKWU9ZS5jb25jYXQodFtzXS5jb21tZW50KTthbGVydChlKSxkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgicHJvZ3Jlc3MiKS5yZXNldCgpLGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzdWNjZXNzZnVsIikuaW5uZXJIVE1MPUpTT04uc3RyaW5naWZ5KHQpLCQoImRpdi5idG4uYnRuLXNtYWxsIilbMV0uY2xpY2soKX0scnVuVGVzdD1mdW5jdGlvbih0LGUsbil7JCgiI3NwdWQiKS5zcHVkKCJhdXRvbWFyayIsdFtlXS5zZXR1cCx0W2VdLnRlc3Qsbil9LHJ1blRlc3RzPWZ1bmN0aW9uKHQsZSl7dmFyIG49MCxzPVtdLG89ZnVuY3Rpb24ocil7cy5wdXNoKHIpLGNvbnNvbGUubG9nKHRbbl0sciksbis9MSxyLmNvbXBsZXRlZCYmbjx0Lmxlbmd0aD9ydW5UZXN0KHQsbixvKTplKHMpfTtydW5UZXN0KHQsbixvKX07JCgiI2F1dG9tYXJrLWJ1dHRvbiIpLmNsaWNrKGZ1bmN0aW9uKCl7cmV0dXJuIHJ1blRlc3RzKHRlc3RzLHNhdmVNYXJrcyksITF9KTs="></script>
	</body>
</html>
EOF
