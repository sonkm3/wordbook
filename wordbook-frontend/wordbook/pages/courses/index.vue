<template>
    <div class="">

        <v-data-table
            :server-items-length="serverItemsLength"
            :headers="headers"
            :items="courses"
            :options.sync="options"
            :loading="loading"
            class="elevation-1"
        >

        <template #top>
            <v-toolbar flat>
                <v-toolbar-title>Courselist</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                    <template #activator="{ on, attrs }">
                        <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                            New Item
                        </v-btn>
                    </template>
                <v-card>
                    <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="editedItem.title" label="title"></v-text-field>
                                    <v-textarea v-model="editedItem.description" label="description"></v-textarea>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>

                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                        Cancel
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="save">
                        Save
                    </v-btn>
                    </v-card-actions>
                </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                        <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                        <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-toolbar>
        </template>

        <template #item.actions="{item}">
            <v-icon class="mr-2" @click.stop="goToWords(item)">
                mdi-clipboard-text-outline
            </v-icon>
            <v-icon class="mr-2" @click.stop="goToPractice(item)">
                mdi-play-circle
            </v-icon>
            <v-icon class="mr-2" @click.stop="editItem(item)">
                mdi-pencil
            </v-icon>
            <v-icon @click.stop="deleteItem(item)">
                mdi-delete
            </v-icon>
        </template>

        </v-data-table>
    </div>
</template>

<script>
export default {
    name: "Courses",
    middleware: 'auth',

    data() {
        return {
            courses: [],
            loading: true,
            serverItemsLength: 1,
            options: {
                page: 1,
                itemsPerPage: 10,
                sortBy:['id'],
                sortDesc:[true],
            },
            headers: [
                { text: "id", value: "id" },
                { text: "title", value: "title" },
                { text: "description", value: "description" },
                { text: 'Actions', value: 'actions', sortable: false },
            ],

            dialog: false,
            dialogDelete: false,

            editedIndex: -1,
            editedItem: {
                title: '',
                description: '',
            },
            defaultItem: {
                title: '',
                description: '',
            },
        };
    },
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
        options: {
            handler() {
                this.$nextTick(function () {
                    this.readDataFromAPI();
                });
            },
        },
        dialog (val) {
            val || this.close()
        },
        dialogDelete (val) {
            val || this.closeDelete()
        },
        deep: true,
    },
    mounted() {
        this.readDataFromAPI();
    },
    methods: {
        readDataFromAPI() {
            this.loading = true;
            const sortBy = this.options.sortBy[0];
            const sortDesc = this.options.sortDesc[0];
            this.$axios.get(
                '/courses/',
                {
                    params:{
                        'page': this.options.page,
                        'count': this.options.itemsPerPage,
                        'ordering': (sortDesc ? '':'-') + sortBy
                    }
                }
            ).then((response) => {
                this.loading = false;
                this.courses = response.data.data;
                this.serverItemsLength = response.data.total;
            });
        },
        updateDataToAPI(itemToUpdate) {
            this.loading = true;
            this.$axios.patch(
                `/courses/${itemToUpdate.id}/`,
                {'title': itemToUpdate.title, 'description': itemToUpdate.description}
            ).then((response) => {
                this.loading = false;
                return true;
            }).catch((response) => {
                this.loading = false;
                return false;
            });
        },
        async postDataToAPI(itemToUpdate) {
            this.loading = true;
            const response = await this.$axios.post(
                '/courses/',
                {'title': itemToUpdate.title, 'description': itemToUpdate.description}
            )
            this.loading = false;
            return response.data;
        },
        deleteDataToAPI(itemToUpdate) {
            this.loading = true;
            this.$axios.delete(
                `/courses/${itemToUpdate.id}/`,
            ).then((response) => {
                this.loading = false;
                return true;
            }).catch((response) => {
                this.loading = false;
                return false;
            });
        },
        editItem (item) {
            this.editedIndex = this.courses.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialog = true;
        },
        deleteItem (item) {
            this.editedIndex = this.courses.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },
        deleteItemConfirm () {
            this.deleteDataToAPI(this.editedItem)
            this.courses.splice(this.editedIndex, 1);
            this.closeDelete();
        },
        close () {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            })
        },
        closeDelete () {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedIndex = -1;
                this.readDataFromAPI();
            })
        },
        save () {
            if (this.editedIndex > -1) {
                this.updateDataToAPI(this.editedItem)
                Object.assign(this.courses[this.editedIndex] , this.editedItem);
            } else {
                this.$nextTick(function () {
                    this.postDataToAPI(this.editedItem).then((createdItem) => {                
                        this.readDataFromAPI();
                    })
                })
            }
            this.close()
        },
        goToWords (row){
            this.$router.push(`/courses/${row.id}/words/`);
        },
        goToPractice (row){
            this.$router.push(`/courses/${row.id}/words/practice/`);
        },

    },
};
</script>
