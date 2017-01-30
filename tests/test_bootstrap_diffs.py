import nimble.utilities.bootstrap_diffs as diffs


def test_bootstrap_diffs():
    first = [
        'one',
        'two',
        'three',
        'four',
        'This is a long line with only a few changes',
        'control end',
    ]
    second = [
        'one',
        'three',
        'four',
        'five'
        'This is a long line with only some changes',
        'control end',
        'new end'
    ]
    table = diffs.bootstrap_diffs(first, second)
    assert table == (
        '<table class="table">'
        # First Row
        '<tr class="blank" style="font-family:monospace;">'
        '<td></td><td>one</td></tr>'
        # Second Row
        '<tr class="danger" style="font-family:monospace;"><td>'
        '<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>'
        '</td><td>two</td></tr>'
        # Row 3
        '<tr class="blank" style="font-family:monospace;">'
        '<td></td><td>three</td></tr>'
        # Row 4
        '<tr class="blank" style="font-family:monospace;">'
        '<td></td><td>four</td></tr>'
        # Row 5
        '<tr class="warning" style="font-family:monospace;"><td>'
        '<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>'
        '</td><td>This is a long line with only <strong>a f</strong>e'
        '<strong>w</strong> changes</td></tr>'
        # Row 6
        '<tr class="warning" style="font-family:monospace;">'
        '<td><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>'
        '</td><td><strong>five</strong>This is a long line with only '
        '<strong>som</strong>e changes</td></tr>'
        # Row 7
        '<tr class="blank" style="font-family:monospace;">'
        '<td></td><td>control end</td></tr>'
        # Row 8
        '<tr class="success" style="font-family:monospace;">'
        '<td><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>'
        '</td><td>new end</td></tr></table>'
    )
