#!/usr/bin/perl
# Kainos regex judge (ADR-0009) — PERL is the canonical regex engine.
#
# Protocol:
#   argv[1]  : the PCRE pattern (as a single argument; no shell-quoting issues)
#   stdin    : lines "1<TAB>example" (must full-match) / "0<TAB>example"
#              (must NOT full-match); examples may be empty strings
#   stdout   : JSON verdict
#              {"ok": bool, "mismatches": [{"text", "expected", "got", "note"}],
#               "compile_error": str?}
#
# The pattern is full-matched: \A(?:pattern)\z — "matches the intended
# language" is decided by execution, not by plausibility.
use strict;
use warnings;

my $pattern = defined $ARGV[0] ? $ARGV[0] : "";

sub jstr {
    my ($s) = @_;
    $s = "" unless defined $s;
    $s =~ s/\\/\\\\/g;
    $s =~ s/"/\\"/g;
    $s =~ s/\n/\\n/g;
    $s =~ s/\r/\\r/g;
    $s =~ s/\t/\\t/g;
    $s =~ s/([\x00-\x1f])/sprintf("\\u%04x", ord($1))/ge;
    return "\"$s\"";
}

my @mismatches;
my $compile_error;
my $re;

$re = eval { qr/\A(?:$pattern)\z/ };
$compile_error = $@ if $@;

while (my $line = <STDIN>) {
    chomp $line;
    my ($exp, $text) = split(/\t/, $line, 2);
    $text = "" unless defined $text;
    my $expected = ($exp eq "1") ? 1 : 0;
    if (!$re) {
        push @mismatches, {
            text     => $text,
            expected => $expected,
            got      => 0,
            note     => "pattern did not compile: $compile_error",
        };
        next;
    }
    my $got = ($text =~ $re) ? 1 : 0;
    if (($got == 1) != ($exp eq "1")) {
        my $note = ($exp eq "1")
            ? "expected match, got no match"
            : "expected no match, got a match";
        push @mismatches, {
            text     => $text,
            expected => $expected,
            got      => $got,
            note     => $note,
        };
    }
}

binmode(STDOUT, ":utf8");
print "{\"ok\":", (@mismatches ? "false" : "true"), ",\"mismatches\":[";
{
    my $first = 1;
    for my $m (@mismatches) {
        print "," unless $first;
        $first = 0;
        my $exp = ($m->{expected} ? "true" : "false");
        my $got = ($m->{got} ? "true" : "false");
        print "{\"text\":",   jstr($m->{text}),
              ",\"expected\":$exp, \"got\":$got,",
              "\"note\":",   jstr($m->{note}), "}";
    }
}
if ($compile_error) {
    print ",\"compile_error\":", jstr($compile_error);
}
print "]}";
print "\n";
exit 0;
