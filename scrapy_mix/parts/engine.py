"""
class Engine
"""
class Engine:
    """
    class Engine
    """
    def __init__(self, manager, stacker, en_id) -> None:
        self.stacker = stacker
        self.curr_node = None
        self.manager = manager
        self.en_id = en_id

    async def core(self):
        while not self.stacker.empty():
            self.curr_node = self.stacker.get()
            self.manager.clawer.midware_manager.process_request(request=self.curr_node)
            self.curr_node = await self.manager.clawer.downloader_manager.download(self.curr_node)
            if self.manager.is_error(request=self.curr_node[0]):
                return
            self.manager.clawer.midware_manager.process_response(response=self.curr_node[1])
            self.manager.tree_callback(engine=self, request=self.curr_node[0], response=self.curr_node[1])

            process_item_task = await self.manager.clawer.pipe_manager.process_items()
        else:
            try:
                await process_item_task
            except Exception as e:
                pass
            self.manager.workshop.put(self)
        