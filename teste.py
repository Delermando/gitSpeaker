def groupRows( rows, rowsNumber, contentRowsNumber):
    groups = []
    group = ''
    times = (contentRowsNumber/rowsNumber)
    if (contentRowsNumber % rowsNumber ) != 0:
        times += 1

    for time in range(0, contentRowsNumber, rowsNumber):
        for row in rows[ time : time + rowsNumber]:
            group += row + '\n'
        groups.append(group)
        group = ''
    return groups


content = r"""
        !/usr/bin/env python
    
        if ( ! current_user_can('manage_links') )
            wp_link_manager_disabled_message();
    
        if ( !empty($_POST['deletebookmarks']) )
            $action = 'deletebookmarks';
        if ( !empty($_POST['move']) )
            $action = 'move';
        if ( !empty($_POST['linkcheck']) )
            $linkcheck = $_POST['linkcheck'];
        if ( !empty($_POST['linkcheck']) )  
            $linkcheck = $_POST['linkcheck'];
        """

#content = gitFileGetContent(os.environ.get('GITSPEAKER_GH_REPOSITORYNAME'), os.environ.get('GITSPEAKER_GH_FIRSTFILENAME'))
contentGroups = groupRows(content.splitlines(), 10, content.count('\n'))
print(len(contentGroups))

