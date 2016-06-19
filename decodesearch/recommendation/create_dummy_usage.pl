#! /usr/bin/perl

use POSIX qw(math_h);

my $tracks = [ "DEV","DBP","INF","CLT","PRD","ARC","DOO","SPL","CHK" ];

my $sessions = {
    "DEV" => [  
        "DEV-001", "DEV-002", "DEV-003", "DEV-004", "DEV-005", "DEV-006", "DEV-007", "DEV-008",
        "DEV-009", "DEV-010", "DEV-011", "DEV-012", "DEV-013", "DEV-014", "DEV-015", "DEV-016",
        "DEV-017", "DEV-018", "DEV-019", "DEV-020", "DEV-021", "DEV-022", "DEV-023", 
    ],
    "DBP" => [
        "DBP-001", "DBP-002", "DBP-003", "DBP-004", "DBP-005", "DBP-006", "DBP-007", "DBP-008",
        "DBP-009", "DBP-010", "DBP-011", "DBP-012", "DBP-013", "DBP-014", "DBP-015", "DBP-016",
        "DBP-017", "DBP-018", "DBP-019", 
    ],
    "INF" => [  
        "INF-001", "INF-002", "INF-003", "INF-004", "INF-005", "INF-006", "INF-007", "INF-008",
        "INF-009", "INF-010", "INF-011", "INF-012", "INF-013", "INF-014", "INF-015", "INF-016",
        "INF-017", "INF-018", "INF-019", "INF-020", "INF-021", "INF-022", "INF-023", "INF-024",
        "INF-025", "INF-026", "INF-027", "INF-028", 
    ],
    "CLT" => [  
        "CLT-001", "CLT-002", "CLT-003", "CLT-004", "CLT-005", "CLT-006", "CLT-007", "CLT-008",
        "CLT-009", "CLT-010", "CLT-011", "CLT-012", "CLT-013", "CLT-014", "CLT-015",
    ],
    "PRD" => [  
        "PRD-001", "PRD-002", "PRD-003", "PRD-004", "PRD-005", "PRD-006", "PRD-007", "PRD-008",
        "PRD-009", "PRD-010",
    ],
    "ARC" => [  
        "ARC-001", "ARC-002", "ARC-003", "ARC-004", "ARC-005", "ARC-006", "ARC-007", "ARC-008",
        "ARC-009", 
   ],
    "DOO" => [  
        "DOO-001", "DOO-002", "DOO-003", "DOO-004", "DOO-005", "DOO-006", "DOO-007", "DOO-008",
        "DOO-009", "DOO-010", "DOO-011", "DOO-012", "DOO-013", "DOO-014", "DOO-015", "DOO-016",
    ],
    "SPL" => [  
        "SPL-001", "SPL-002", "SPL-003", "SPL-004", "SPL-005",
    ],
    "CHK" => [  
        "CHK-001", "CHK-002", "CHK-003", "CHK-004", "CHK-005", "CHK-006", "CHK-007", "CHK-008",
        "CHK-009", 
    ]
};


$argc = $#ARGV + 1;

if ($argc !=2 ) {
    print "Usage: $0 <usernum> <clicknum>\n";
    print "  <usernum> - number of user who use this services\n";
    print "  <clicknum> - number of clicks that each use do\n";
    exit 1;
}

my $usernum =$ARGV[0];
my $clicknum =$ARGV[1];
my $u = 1;my $c=1;
while( $u < $usernum ){
    $c=1;
    while( $c < $clicknum ){
        print STDOUT $u . "," . getrandomsession(getrandomtrack()) . "\n";
        $c++;
    }
    $u++;
}

sub getrandomtrack
{
    my $total = scalar @$tracks;
    return @$tracks[getrandom($total)];
}

sub getrandomsession
{
    my $track = shift;
    my $ss = $sessions->{$track};
    my $total = scalar @$ss;
    my $random = getrandom($total); 
    return @$ss[$random];
}

sub getrandom
{
    my $max = shift;
    my $r = rand();
    return floor( $max * $r );
}

__END__
