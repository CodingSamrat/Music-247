def base_help_message(prefix, guild_name):
    msg = f"""
    ```
    
    Guild: {guild_name}
    Command Prefix: {prefix}

    These are some common Bot commands:

        Group Command           Descriptions
        -----------             ----------------
        config, cfg             Modify server config
        music, m                Handle music system
        
        
        Standalone Command      Descriptions
        ------------------      ----------------
        ping                    Shows bot latency
        help, h                 Shows this message     

        Group Commands have some sub-commands. 
        Run them to know more.
        
    ```    
    """

    return msg


def config_help_message(prefix, guild_name, root_cmd):
    msg = f"""
    ```
    
    Guild: {guild_name}
    Command Prefix: {prefix}
    Root Command: {root_cmd}

    These are common `{prefix}{root_cmd}` commands:

        Command                 Descriptions
        -----------             ----------------
        config, cfg             Shows this message [root]    
        prefix                  Change Command Prefix

    ```    
    """

    return msg


def music_help_message(prefix, guild_name, root_cmd):
    msg = f"""
    ```
    
    Guild: {guild_name}
    Command Prefix: {prefix}
    Root Command: {root_cmd}

    These are common `{prefix}{root_cmd}` commands:

        Command                 Descriptions
        -----------             ----------------
        music, m                Shows this message [root]   
        channel                 Created a channel for UI 
        play, p                 Play music
        pause, ps               Pause music
        stop, s                 Stop  music
        resume, r               Resume music
        next, n                 Play next music
        add, a                  Add music to queue
        queue, q                Shows all musics of queue
        
    ```    
    """

    return msg
